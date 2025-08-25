from flask import Blueprint, render_template, redirect, request, url_for, session, flash
from app import db
from app.models import Task 

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def view_tasks():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login')) 
    
    tasks = Task.query.filter_by(user_id=session['user_id']).all()
    return render_template("tasks.html", tasks=tasks)


@tasks_bp.route('/add', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login')) 
    
    title = request.form.get('title')
    if title:
        new_task = Task(title=title, status='pending', user_id=session['user_id'])
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully", 'success')
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_status(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))

    task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()
    if task:
        if task.status == 'pending':
            task.status = 'working'
        elif task.status == 'working':
            task.status = 'done'
        else:
            task.status = 'pending'   # cycle back
        db.session.commit()
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/clear', methods=['POST'])
def clear_task():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))

    Task.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()
    flash("Deleted all your tasks", 'info')
    return redirect(url_for('tasks.view_tasks'))
