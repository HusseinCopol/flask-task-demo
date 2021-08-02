from flask import Flask, render_template,url_for,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///test.db'
db=SQLAlchemy(app)
ma=Marshmallow(app)

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    customer_id=db.Column(db.Integer,nullable=False,default=1)
    date=db.Column(db.DateTime,default=datetime.utcnow)
    status=db.Column(db.String(200),nullable=False,default="Not Delivered")

    def __init__ (self,name,customer_id):
        self.name=name
        self.customer_id=customer_id
    

class OrderSchema(ma.Schema):
    class Meta:
        fields=("id","name","customer_id","date","status")

order_schema=OrderSchema()
orders_schema=OrderSchema(many=True)

def __repr__(self):
    return '<Order %r>' %self.id 







@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST'  :
        if 'add_order' in request.form:
            order_name= request.form['order']
            new_order=Todo(name=order_name)
            try:
                db.session.add(new_order)
                db.session.commit()
                return redirect('/')
            except:
                return 'An Error has occured,The order is not added'
                
        elif 'download_orders' in request.form:
            orders=Todo.query.order_by(Todo.date).all()
            result=orders_schema.dump(orders)
            return jsonify(result)

           
        

    

    else:
        orders=Todo.query.order_by(Todo.date).all()
        return render_template('index.html',orders=orders)

@app.route('/delete/<int:id>')
def delete(id):
    order_to_delete=Todo.query.get_or_404(id)
    
    try:
        db.session.delete(order_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'An Error has occured,your order is not deleted'


@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    order_to_update=Todo.query.get_or_404(id)
    if request.method == "POST":
        order_to_update.name = request.form['order']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'An Error has occured while trying to update your order'
    else:
        return render_template('update.html',order=order_to_update)


#REST
@app.route('/get',methods=['GET'])
def get_orders():
    orders=Todo.query.order_by(Todo.date).all()
    result=orders_schema.dump(orders)
    return jsonify(result)
   


@app.route('/post',methods=['POST'])
def add_orders():

    name=request.json['name']
    customer_id=request.json['customer_id']

    new_order=Todo(name, customer_id)
    db.session.add(new_order)
    db.session.commit()

    return order_schema.jsonify(new_order)

@app.route('/order_details/<id>',methods=['GET'])
def order_details(id):
    order=Todo.query.get(id)
    return order_schema.jsonify(order)


@app.route('/order_update/<id>',methods=['PUT'])
def order_update(id):
    order=Todo.query.get(id)
    order.name=request.json['name']
    order.customer_id=request.json['customer_id']
    order.status=request.json['status']

    db.session.commit()

    return order_schema.jsonify(order)

@app.route('/order_delete/<id>',methods=['DELETE'])
def order_delete(id):
    order=Todo.query.get(id)
    db.session.delete(order)
    db.session.commit()

    return order_schema.jsonify(order)


if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)