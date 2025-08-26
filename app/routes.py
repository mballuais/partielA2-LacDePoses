from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Material, Order, OrderItem

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    materials = Material.query.all()
    orders = Order.query.all()
    return render_template('index.html', materials=materials, orders=orders)

@bp.route('/add_material', methods=['GET', 'POST'])
def add_material():
    if request.method == 'POST':
        try:
            name = request.form['name']
            quantity = int(request.form['quantity'])
            price = float(request.form['price'])
            
            material = Material(
                name=name,
                available_quantity=quantity,
                rental_price=price
            )
            
            db.session.add(material)
            db.session.commit()
            flash('Matériel ajouté avec succès!', 'success')
            return redirect(url_for('main.index'))
            
        except Exception as e:
            flash('Erreur lors de l\'ajout du matériel', 'error')
            db.session.rollback()
    
    return render_template('add_material.html')

@bp.route('/edit_material/<int:id>', methods=['GET', 'POST'])
def edit_material(id):
    material = Material.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            material.name = request.form['name']
            material.available_quantity = int(request.form['quantity'])
            material.rental_price = float(request.form['price'])
            
            db.session.commit()
            flash('Matériel modifié avec succès!', 'success')
            return redirect(url_for('main.index'))
            
        except Exception as e:
            flash('Erreur lors de la modification du matériel', 'error')
            db.session.rollback()
    
    return render_template('edit_material.html', material=material)


@bp.route('/create_order', methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':
        try:
            customer_name = request.form['customer_name']
            
            if not customer_name:
                flash('Le nom du client est obligatoire', 'error')
                return redirect(url_for('main.create_order'))
            
            order = Order(customer_name=customer_name, total_price=0.0)
            db.session.add(order)
            db.session.commit()
            
            flash('Commande créée avec succès!', 'success')
            return redirect(url_for('main.add_to_order', order_id=order.id))
            
        except Exception as e:
            flash('Erreur lors de la création de la commande', 'error')
            db.session.rollback()
    
    return render_template('create_order.html')

@bp.route('/add_to_order/<int:order_id>', methods=['GET', 'POST'])
def add_to_order(order_id):
    order = Order.query.get_or_404(order_id)
    materials = Material.query.filter(Material.available_quantity > 0).all()
    
    if request.method == 'POST':
        try:
            material_id = int(request.form['material_id'])
            quantity = int(request.form['quantity'])
            
            material = Material.query.get_or_404(material_id)

            if quantity > material.available_quantity:
                flash(f'Stock insuffisant. Disponible: {material.available_quantity}', 'error')
                return redirect(url_for('main.add_to_order', order_id=order_id))

            order_item = OrderItem(
                order_id=order.id,
                material_id=material.id,
                quantity=quantity,
                unit_price=material.rental_price
            )

            material.available_quantity -= quantity

            order.total_price += (quantity * material.rental_price)
            
            db.session.add(order_item)
            db.session.commit()
            
            flash(f'{quantity}x {material.name} ajouté à la commande!', 'success')
            
        except Exception as e:
            flash('Erreur lors de l\'ajout à la commande', 'error')
            db.session.rollback()
    
    return render_template('add_to_order.html', order=order, materials=materials)

@bp.route('/return_order/<int:order_id>')
def return_order(order_id):
    try:
        order = Order.query.get_or_404(order_id)

        for item in order.items:
            material = Material.query.get(item.material_id)
            material.available_quantity += item.quantity

        db.session.delete(order)
        db.session.commit()
        
        flash('Commande restituée avec succès!', 'success')
        
    except Exception as e:
        flash('Erreur lors de la restitution', 'error')
        db.session.rollback()
    
    return redirect(url_for('main.index'))

@bp.route('/remove_item/<int:item_id>')
def remove_item(item_id):
    try:
        item = OrderItem.query.get_or_404(item_id)
        order_id = item.order_id

        material = Material.query.get(item.material_id)
        material.available_quantity += item.quantity

        order = Order.query.get(order_id)
        order.total_price -= (item.quantity * item.unit_price)

        db.session.delete(item)
        db.session.commit()
        
        flash(f'{item.quantity}x {material.name} retiré de la commande!', 'success')
        
    except Exception as e:
        flash('Erreur lors de la suppression', 'error')
        db.session.rollback()
    
    return redirect(url_for('main.add_to_order', order_id=order_id))

@bp.route('/stats')
def stats():
    total_materials = Material.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_price)).scalar() or 0
    
    most_rented = db.session.query(
        Material.name,
        db.func.sum(OrderItem.quantity).label('total_rented')
    ).join(OrderItem).group_by(Material.id).order_by(
        db.func.sum(OrderItem.quantity).desc()
    ).first()
    
    return render_template('stats.html',
                         total_materials=total_materials,
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         most_rented=most_rented)