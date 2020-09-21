from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import easygui
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import exists

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Product(db.Model):
    pid = db.Column(db.Integer,autoincrement=True,unique = True)
    name = db.Column(db.String(100),primary_key=True,unique = True)
    loc = db.relationship('Location')
    mov = db.relationship('Movement')
    def __repr__(self):
        return f"Product('{self.name}')"

class Location(db.Model):
    lid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    loc1 = db.Column(db.Integer)
    loc2 = db.Column(db.Integer)
    loc3 = db.Column(db.Integer)
    name = db.Column(db.String(100),db.ForeignKey('product.name'))

    def __repr__(self):
        return f"Location('{self.loc1}','{self.loc2}','{self.loc3}')"

class Movement(db.Model):
    mid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    from_l = db.Column(db.String(100),default="None")
    to_l = db.Column(db.String(100),default="None")
    amount = db.Column(db.Integer)
    quantity = db.Column(db.Integer,default="None")
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    name = db.Column(db.String(100),db.ForeignKey('product.name'))

    def __repr__(self):
        return f"Movement('{self.from_l}','{self.to_l}','{self.amount}','{self.quantity}')"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movement', methods=['GET', 'POST'])
def movement():
    for value in db.session.query(Product.name).distinct():
        all_versions = db.session.query(Location.loc1,Location.loc2,Location.loc3).filter(Location.name == str(value[0]))
        all_version1 = db.session.query(Movement.quantity,Movement.mid).filter(Movement.name == str(value[0]))
        for i in all_versions:
            for j in all_version1:
                l1 = list(i) + list(j)
                id = l1.pop(4)
                l = {}
                l['Bangalore'] = l1[0]
                l['Chennai'] = l1[1]
                l['Mumbai'] = l1[2]
                l['Min'] = l1[3]
                easygui.msgbox(l)
                div = l['Min']
                l.pop('Min')
                key_max = max(l.keys(), key=(lambda k1: l[k1]))
                key_min = min(l.keys(), key=(lambda k1: l[k1]))
                mi = l[key_min]
                ma = l[key_max]

                easygui.msgbox(mi)
                easygui.msgbox(ma)

                l.pop(key_min)
                l.pop(key_max)

                key_me = max(l.keys(), key=(lambda k1: l[k1]))
                me = l[key_me]

                if(mi < div or me < div or ma < div ):
                    easygui.msgbox(ma - (2*(div-mi)))
                    if(mi == me and ma - (2*(div-mi))):
                        easygui.msgbox("Here 2 min values are same")
                        task3 = Movement.query.get_or_404(id)
                        amount = (div-mi)
                        from_l = key_max
                        to_l =  key_min

                        easygui.msgbox(from_l,"From ")
                        easygui.msgbox(to_l,"To ")

                        task3.amount = amount
                        task3.from_l = from_l
                        task3.to_l = to_l

                        try:
                            db.session.commit()
                            #return redirect('movement.html')
                        except:
                            return 'There was an issue updating your task'

                        amount = (div-mi)
                        from_l = key_max
                        to_l = key_me

                        if db.session.query(db.func.max(Movement.mid)).scalar() is not None: #check if id=1 exists
                            mid = db.session.query(db.func.max(Movement.mid)).scalar() + 1
                        else:#else run when no record is present
                            mid = 1
                        easygui.msgbox(from_l,"From ")
                        easygui.msgbox(to_l,"To ")
                        new_mov = Movement(quantity = div,mid = mid,name = str(value[0]), from_l = from_l,to_l = to_l,amount = amount)
                        db.session.add(new_mov)
                        db.session.commit()
                    elif(mi < div and me < div and div < mi -(div-mi + div-me) ):
                        easygui.msgbox("Here 2 min values are diff")
                        task3 = Movement.query.get_or_404(id)
                        amount = (div-mi)
                        from_l = key_max
                        to_l =  key_min

                        easygui.msgbox(from_l,"From ")
                        easygui.msgbox(to_l,"To ")

                        task3.amount = amount
                        task3.from_l = from_l
                        task3.to_l = to_l

                        try:
                            db.session.commit()
                            #return redirect('movement.html')
                        except:
                            return 'There was an issue updating your task'

                        amount = (div-me)
                        from_l = key_max
                        to_l =  key_me 

                        if db.session.query(db.func.max(Movement.mid)).scalar() is not None: #check if id=1 exists
                            mid = db.session.query(db.func.max(Movement.mid)).scalar() + 1
                        else:#else run when no record is present
                            mid = 1
                        easygui.msgbox(from_l,"From ")
                        easygui.msgbox(to_l,"To ")
                        new_mov = Movement(quantity = div,mid = mid,name = str(value[0]), from_l = from_l,to_l = to_l,amount = amount)
                        db.session.add(new_mov)
                        db.session.commit()
                    elif(mi < div and div < ma - (div-mi) ):
                        easygui.msgbox("Only one min")
                        task3 = Movement.query.get_or_404(id)
                        amount = (div-mi)
                        from_l = key_max
                        to_l =  key_min

                        easygui.msgbox(from_l,"From ")
                        easygui.msgbox(to_l,"To ")

                        task3.amount = amount
                        task3.from_l = from_l
                        task3.to_l = to_l

                        try:
                            db.session.commit()
                            #return redirect('movement.html')
                        except:
                            return 'There was an issue updating your task'

                    else:
                        task_to_delete = Movement.query.get_or_404(id)

                        try:
                            db.session.delete(task_to_delete)
                            db.session.commit()
                            #return redirect('/')
                        except:
                            return 'There was a problem deleting that task'
                else:
                    task3 = Movement.query.order_by(Movement.mid).all()
                    #return render_template('movement.html',task3 = task3)
    task3 = Movement.query.order_by(Movement.mid).all()
    return render_template('movement.html',task3 = task3)

@app.route('/code', methods=['GET', 'POST'])
def code():
    if request.method == 'POST':
        return redirect(url_for('index'))
    task1 = Product.query.order_by(Product.pid).all()
    task2 = Location.query.order_by(Location.lid).all()
    task3 = Movement.query.order_by(Movement.mid).all()
        

    return render_template('code.html',task1 = task1,task2 = task2,task3 = task3)

@app.route('/additem', methods=['GET', 'POST'])
def additem():
    if request.method == 'POST':
        task_content = request.form['prod']
        
        if db.session.query(db.func.max(Product.pid)).scalar() is not None: #check if id=1 exists
            pid = db.session.query(db.func.max(Product.pid)).scalar() + 1
        else:#else run when no record is present
            pid = 1
        
        if db.session.query(db.func.max(Location.lid)).scalar() is not None: #check if id=1 exists
            lid = db.session.query(db.func.max(Location.lid)).scalar() + 1
        else:#else run when no record is present
            lid = 1
        
        if db.session.query(db.func.max(Movement.mid)).scalar() is not None: #check if id=1 exists
            mid = db.session.query(db.func.max(Movement.mid)).scalar() + 1
        else:#else run when no record is present
            mid = 1
        task_content2 = request.form['quant']

        new_task = Product(name = task_content,pid = pid)

        task_content1 = request.form['l1']
        task_content3 = request.form['l2']
        task_content4 = request.form['l3']
        new_loc1 = Location(loc1 = task_content1,loc2 = task_content3,loc3 = task_content4,lid = lid,name = task_content)
        new_mov = Movement(quantity = task_content2,mid = mid,name = task_content)
        easygui.msgbox(new_loc1)
        
        try:
            #session = sessionLoader()
            db.session.add(new_task)
           # db.session.commit()
            db.session.add(new_loc1)
            #db.session.commit()
            #db.session.add(new_loc2)
            #db.session.commit()
            ##db.session.add(new_loc3)
            #db.session.commit()
            db.session.add(new_mov)
            db.session.commit()
            easygui.msgbox("Item is added", title="Added")   
            return redirect(url_for('additem'))
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error
    else:
        return render_template('additem.html')
@app.route('/location', methods=['GET', 'POST'])
def location():
    return render_template('location.html')

@app.route('/update_p', methods=['GET', 'POST'])
def update_p():
    if request.method == 'POST':
        return redirect(url_for('update_p.html'))

    return render_template('update_p.html')

@app.route('/delete/<string:name>')
def delete(name):

    all_versions = db.session.query(Location.lid).filter(Location.name == name)
    all_version1 = db.session.query(Movement.mid).filter(Movement.name == name)
    all_version2 = db.session.query(Product.pid).filter(Product.name == name)

    db.session.delete(all_version1)
    db.session.delete(all_versions)
    db.session.delete(all_version2)
    
    db.session.commit()

@app.route('/update', methods=['GET', 'POST'])
def update():
    easygui.msgbox("Here")
    if request.method == 'POST':
        name = request.form['prod']
        
        loc1 = request.form['l1']
        loc2 = request.form['l2']
        loc3 = request.form['l3']

        quant = request.form['quant']

        all_versions = db.session.query(Location.lid).filter(Location.name == name)
        all_version1 = db.session.query(Movement.mid).filter(Movement.name == name)
        all_version2 = db.session.query(Product.pid).filter(Product.name == name)

        for i in all_version1:
            task3 = Movement.query.get_or_404(i)
            task3.name = name
            task3.quantity = quant
        for i in all_versions:
            task2 = Location.query.get_or_404(i)
            task2.name = name
            task2.loc1 = loc1
            task2.loc2 = loc2
            task2.loc3 = loc3
        for i in all_version2:
            task1 = Product.query.get_or_404(i)
            task1.name = name
        
        easygui.msgbox("Updated")
        try:
            db.session.commit()
            return redirect('code.html')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)