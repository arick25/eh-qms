from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from models import Base, Document, Audit, CAPA, User, Material, Employee
import os

def setup_routes(app):
    # Set up database session
    engine = create_engine('sqlite:///qms.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # Login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = session.query(User).filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                return "Invalid credentials"
        return render_template('login.html')

    # Logout
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    # Registration
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user:
                return "Username already exists"
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            session.add(new_user)
            session.commit()
            return redirect(url_for('login'))
        return render_template('register.html')

    # Dashboard
    @app.route('/')
    @login_required
    def dashboard():
        documents = session.query(Document).all()
        return render_template('dashboard.html', documents=documents)

    # Upload Document
    @app.route('/upload', methods=['GET', 'POST'])
    @login_required
    def upload():
        if request.method == 'POST':
            file = request.files['file']
            title = request.form['title']
            version = request.form['version']
            owner = request.form['owner']
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            doc = Document(
                title=title,
                version=version,
                owner=owner,
                date_created=date.today(),
                file_path=filepath
            )
            session.add(doc)
            session.commit()
            return redirect(url_for('dashboard'))

        return render_template('upload.html')

    # Audits
    @app.route('/audits')
    @login_required
    def audits():
        audit_list = session.query(Audit).all()
        return render_template('audits.html', audits=audit_list)

    @app.route('/audit/new', methods=['GET', 'POST'])
    @login_required
    def new_audit():
        if request.method == 'POST':
            audit = Audit(
                area=request.form['area'],
                auditor=request.form['auditor'],
                findings=request.form['findings'],
                corrective_action=request.form['corrective_action'],
                date=date.today(),
                status=request.form['status']
            )
            session.add(audit)
            session.commit()
            return redirect(url_for('audits'))
        return render_template('new_audit.html')

    # CAPAs
    @app.route('/capa')
    @login_required
    def capa_list():
        capas = session.query(CAPA).all()
        return render_template('capa.html', capas=capas)

    @app.route('/capa/new', methods=['GET', 'POST'])
    @login_required
    def new_capa():
        if request.method == 'POST':
            capa = CAPA(
                issue=request.form['issue'],
                root_cause=request.form['root_cause'],
                corrective_action=request.form['corrective_action'],
                preventive_action=request.form['preventive_action'],
                owner=request.form['owner'],
                date_created=date.today(),
                status=request.form['status'],
                effectiveness_review=request.form['effectiveness_review']
            )
            session.add(capa)
            session.commit()
            return redirect(url_for('capa_list'))
        return render_template('new_capa.html')

    # KPI Dashboard
    @app.route('/kpi')
    @login_required
    def kpi_report():
        capa_total = session.query(CAPA).count()
        capa_open = session.query(CAPA).filter_by(status='Open').count()
        capa_monitoring = session.query(CAPA).filter_by(status='Monitoring').count()
        capa_closed = session.query(CAPA).filter_by(status='Closed').count()

        audit_total = session.query(Audit).count()
        audit_open = session.query(Audit).filter_by(status='Open').count()
        audit_closed = session.query(Audit).filter_by(status='Closed').count()

        doc_total = session.query(Document).count()

        return render_template('kpi.html', 
            capa_total=capa_total,
            capa_open=capa_open,
            capa_monitoring=capa_monitoring,
            capa_closed=capa_closed,
            audit_total=audit_total,
            audit_open=audit_open,
            audit_closed=audit_closed,
            doc_total=doc_total
        )

    # Inventory
    @app.route('/inventory')
    @login_required
    def inventory():
        materials = session.query(Material).all()
        return render_template('inventory.html', materials=materials)

    @app.route('/inventory/new', methods=['GET', 'POST'])
    @login_required
    def new_material():
        if request.method == 'POST':
            material = Material(
                type=request.form['type'],
                gauge=request.form['gauge'],
                thickness=request.form['thickness'],
                length=request.form['length'],
                width=request.form['width'],
                quantity=int(request.form['quantity'])
            )
            session.add(material)
            session.commit()
            return redirect(url_for('inventory'))
        return render_template('new_material.html')

    # Employees
    @app.route('/employees')
    @login_required
    def employee_list():
        employees = session.query(Employee).all()
        return render_template('employees.html', employees=employees)

    @app.route('/employee/new', methods=['GET', 'POST'])
    @login_required
    def new_employee():
        if request.method == 'POST':
            employee = Employee(
                name=request.form['name'],
                title=request.form['title'],
                department=request.form['department'],
                status=request.form['status'],
                pay_rate=request.form['pay_rate'],
                hire_date=date.fromisoformat(request.form['hire_date']),
                contact=request.form['contact']
            )
            session.add(employee)
            session.commit()
            return redirect(url_for('employee_list'))
        return render_template('new_employee.html')
