from ..models.med import Med
from flask_app.models.patient import Patient
from flask_app.models.pharmacy import Pharmacy
from flask_app import app
from flask import redirect, render_template, session, request, flash

@app.route("/patient_profile/<int:patient_id>/<int:pharmacy_id>")
def show_all_meds_one_patient_one_pharmacy(patient_id, pharmacy_id):
    if 'patient_id' in session and session['patient_id'] == patient_id:
        data = {
            'patient_id' : patient_id,
            'pharmacy_id' : pharmacy_id
        }
        return render_template("patient_meds.html", all_meds = Med.get_all_meds_one_patient_one_pharmacy(data), one_pharmacy = Pharmacy.get_one_pharmacy({"id":pharmacy_id}), one_patient = Patient.get_one_patient({"id": patient_id}))
    else:
        flash('Please sign in to access your profile!','patient_login')
        return redirect('/patients')

@app.route("/new_med/<int:patient_id>/<int:pharmacy_id>")
def add_patient_prescription(patient_id, pharmacy_id):
    if 'patient_id' in session and session['patient_id'] == patient_id:
        return render_template('add_prescription.html', one_patient = Patient.get_one_patient({"id": patient_id}), one_pharmacy = Pharmacy.get_one_pharmacy({"id":pharmacy_id}))
    else:
        flash('Please sign in to access your profile!','patient_login')
        return redirect('/patients')

@app.route("/new_med/<int:patient_id>")
def add_prescription_any_pharmacy(patient_id):
    if 'patient_id' in session and session['patient_id'] == patient_id:
        all_pharmacies = Pharmacy.get_all_pharmacies()
        for one_pharmacy in all_pharmacies:
            print(one_pharmacy.id)
        return render_template('add_prescription_any_pharmacy.html', one_patient = Patient.get_one_patient({"id": patient_id}), all_pharmacies = Pharmacy.get_all_pharmacies())
    else:
        flash('Please sign in to access your profile!','patient_login')
        return redirect('/patients')

@app.route("/add_prescription/<int:patient_id>/<int:pharmacy_id>", methods=['POST'])
def add_prescription(patient_id, pharmacy_id):
    if 'patient_id' in session and session['patient_id'] == patient_id:
        print(type(request.form['days_left']))
        if not Med.validate_inputs(request.form):
            return redirect(f'/new_med/{patient_id}/{pharmacy_id}')
        data = {
            'name' : request.form['name'],
            'directions' : request.form['directions'],
            'days_left': request.form['days_left'],
            'refills': request.form['refills'],
            'patient_id' : patient_id,
            'pharmacy_id' : pharmacy_id,
            'refill_request': 0
        }
        Med.save(data)
    return redirect(f"/patient_profile/{patient_id}/{pharmacy_id}")

@app.route("/add_prescription/<int:patient_id>", methods= ['POST'])
def add_rx_any_pharmacy(patient_id):
    if 'patient_id' in session and session['patient_id'] == patient_id:
        if not Med.validate_inputs(request.form):
            return redirect(f'/new_med/{patient_id}')
        data = {
            'name' : request.form['name'],
            'directions' : request.form['directions'],
            'days_left': request.form['days_left'],
            'refills': request.form['refills'],
            'patient_id' : patient_id,
            'pharmacy_id' : request.form['pharmacy'],
            'refill_request': 0
        }
        Med.save(data)
    return redirect(f"/patient_profile/{patient_id}")


@app.route("/request_refill/all_meds_view/<int:patient_id>/<int:pharmacy_id>/<int:id>")
def request_refill_all_meds_view(patient_id, pharmacy_id, id):
    if 'patient_id' in session and session['patient_id'] == patient_id:
        print(id)
        data = {
            'id' : id
        }
        medication = Med.get_one_med(data)
        refill = Med.requestRefill(data)
        return redirect(f"/patient_profile/{patient_id}")
    else:
        flash('Please sign in to access your profile!','patient_login')
        return redirect('/patients')

@app.route("/request_refill/one_pharamcy_view/<int:patient_id>/<int:pharmacy_id>/<int:id>")
def request_refill_one_pharamcy_view(patient_id, pharmacy_id, id):
    if 'patient_id' in session and session['patient_id'] == patient_id:
        print(id)
        data = {
            'id' : id
        }
        medication = Med.get_one_med(data)
        refill = Med.requestRefill(data)
        return redirect(f"/patient_profile/{patient_id}/{pharmacy_id}")
    else:
        flash('Please sign in to access your profile!','patient_login')
        return redirect('/patients')


@app.route('/delete_meds/one_pharmacy_view/<int:patient_id>/<int:pharmacy_id>/<int:id>')
def deleteMeds_one_pharamcy_view(patient_id, pharmacy_id, id):
    if 'patient_id' in session and session['patient_id'] == patient_id:
        data ={
            'id': id
        }
        Med.delete(data)
        return redirect(f'/patient_profile/{patient_id}/{pharmacy_id}')
    else:
        flash('Please sign in to access your profile!','patient_login')
        return redirect('/patients')

@app.route('/delete_meds/all_meds_view/<int:patient_id>/<int:pharmacy_id>/<int:id>')
def deleteMeds_all_meds_view(patient_id, pharmacy_id, id):
    if 'patient_id' in session and session['patient_id'] == patient_id:
        data ={
            'id': id
        }
        Med.delete(data)
        return redirect(f'/patient_profile/{patient_id}')
    else:
        flash('Please sign in to access your profile!','patient_login')
        return redirect('/patients')