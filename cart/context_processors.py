from .cart import Cart

def cart(request):
    return {'cart': Cart(request)}

#this will make the cart avalible evrywhere