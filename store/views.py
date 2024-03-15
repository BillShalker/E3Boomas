from django.shortcuts import render, redirect
from .models import CartItem, Product
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


def view_cart(request):
    # Получаем корзину из сессии или инициализируем пустую корзину
    cart = request.session.get('cart', {})

    # Извлекаем ID продуктов из корзины для получения объектов из базы данных
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    # Создаем список элементов корзины, добавляя информацию о продукте
    cart_items = []
    total_price = 0
    for product in products:
        item = {
            'name': product.title,
            'quantity': cart[str(product.id)]['quantity'],
            'price': cart[str(product.id)]['price'],
            'total_price': cart[str(product.id)]['quantity'] * cart[str(product.id)]['price'],
            'id': product.id
        }
        cart_items.append(item)
        total_price += item['total_price']

    # Если запрос является AJAX-запросом, можно вернуть только данные корзины в JSON,
    # в противном случае — рендерим страницу с корзиной как обычно.
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Для AJAX-запросов возвращаем данные в формате JSON
        from django.http import JsonResponse
        return JsonResponse({
            'cart_items': cart_items,
            'total_price': total_price
        })
    else:
        # Для обычных запросов возвращаем отрендеренный шаблон
        return render(request, 'store/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


def add_to_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, pk=product_id)
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += quantity
        else:
            cart[str(product_id)] = {'quantity': quantity, 'price': float(product.price)}

        request.session['cart'] = cart

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Подготовьте данные о корзине для отправки обратно на клиент
            return JsonResponse({
                'total_items': sum(item['quantity'] for item in request.session['cart'].values()),
                # Добавьте другие необходимые данные
            })

    return redirect('view_cart')


def remove_from_cart(request, item_id):
    CartItem.objects.filter(user=request.user, pk=item_id).delete()
    return redirect('view_cart')


def update_cart(request):
    CartItem.objects.filter(user=request.user).update(quantity=1)
    return redirect('view_cart')
