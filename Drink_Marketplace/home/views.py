from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from product.models import Product, Comment
from product.forms import CommentForm
from support_ai.ai_utils import predict_support_ensemble
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
with open('vietnamese_stopwords.txt', 'r', encoding='utf-8') as f:
    stopwords = set(f.read().splitlines())

# Hàm tiền xử lý văn bản
def preprocess_text(text):
    text = re.sub(r'[^\w\s]', ' ', text)  # loại ký tự đặc biệt
    text = text.lower()
    words = text.split()
    words = [word for word in words if word not in stopwords]
    return ' '.join(words)

def Get_home(request):
    products = Product.objects.all()
    return render(request, 'home/home.html', {'products': products})# Truyền vào template

def update_comment_status(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment.status = request.POST.get('status')
        comment.note = request.POST.get('note', '')
        comment.save()
    return redirect('support_message')

@staff_member_required
def support_messages(request):
    comments = Comment.objects.filter(needs_support=True).order_by('-created_at')
    return render(request, 'home/support_message.html', {'comments': comments})
def is_admin(user):
    return user.is_superuser
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    comments = Comment.objects.filter(product=product).order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.needs_support = predict_support_ensemble(comment.content)            
            comment.save()
            form = CommentForm()
    else:
        form = CommentForm()

    # === Gợi ý sản phẩm tương tự ===
    all_products = Product.objects.all()
    
    # Gộp name + description và xử lý text
    combined_texts = []
    for p in all_products:
        combined = (p.name or '') + ' ' + (p.description or '')
        processed = preprocess_text(combined)
        combined_texts.append(processed)

    tfidf = TfidfVectorizer().fit_transform(combined_texts)
    cosine_similarities = cosine_similarity(tfidf)

    idx = list(all_products).index(product)
    sim_scores = list(enumerate(cosine_similarities[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [i for i in sim_scores if i[0] != idx][:3]
    similar_products = [all_products[i[0]] for i in sim_scores]

    return render(request, 'home/product_detail.html', {
        'product': product,
        'comments': comments,
        'form': form,
        'similar_products': similar_products,
    })
