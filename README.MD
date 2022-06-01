# db_lab3

## Посилання на розгорнутий проект:
https://lanovenko-db-lab3.herokuapp.com/

## Інструкція по розгортанню:
1. Завантажити `Heroku Toolelt CLI` з https://devcenter.heroku.com/articles/heroku-cli
2. Відкрити консоль з проектом
3. `pip install gunicorn`
4. Створити `Procfile` та вписати всередину `web: gunicorn app:app`
5. Створити файл з необхідними залежностями: pip freeze > requirements.txt
6. Авторизуватися: `heroku login`
7. Створити проект: `heroku create <app_name>`
8. Створити БД: `heroku addons:create heroku-postgresql:hobby-dev --app <app_name>`
9. Отримати DATABASE_URL за допомогою `heroku config --app <app_name>` та встановити його у програмі
10. Відправити зміни у віддалений репозиторій: `git add .`, `git commit -m "Initial commit"`, `git push проекта на GitHub`
11. Відправити гілку `main` на сервер heroku: `git push heroku main`
12. Запустити python консоль: `heroku run python`
13. Створити сутності в БД: `from app import db`, `db.ceate_all()`, `exit()`
14. Enjoy!)
