from website import create_app, db
from website.models import User, Role, Style

app = create_app()

with app.app_context():
    admin_role = Role(name='admin', description='Имеет полный доступ к системе, в том числе к созданию и удалению книг')
    mod_role = Role(name='mod', description='Может редактировать данные книг и производить модерацию рецензий')
    user_role = Role(name='user', description='Может оставлять рецензии')


    db.session.add_all([admin_role, mod_role, user_role])
    db.session.commit() 


    kirillbad_user = User(login='kirillbad', password_hash='scrypt:32768:8:1$T7aWszDpoq1TphZm$3d780ce93e1722a7208431e3a878c1b93d17c90209672bb2e5259670037e66a1c3cdb5e86670a2a1b379033effeea49924bcc60f1680ca7746c0dc81584ca308', last_name='Баденов', first_name='Кирилл', middle_name='Дмитриевич', role=admin_role)
    BluePencilBoard_user = User(login='BluePencilBoard', password_hash='scrypt:32768:8:1$2uJa8uqacopXn6Mz$ebab945a95013fefc5cf83ce34e67cb115f4379af898dba5ffb3d926bef892b519548ce30c7718dc4c7ed2e99715982b37e8dffc81377e6b20b446bacafad06b', last_name='Ахмадов', first_name='Сайд-Эмин', middle_name='Абдрашидович', role=mod_role)
    Jerold_user = User(login='Jerold', password_hash='scrypt:32768:8:1$H2ddVGWCQlEnEXgE$65d09d9df6f69e306e4065cedd2e83b4619c84993db562a3a44477464173e17193e52eaa823ce60e16210fef7e5dd3fc49cad71cf246ddd015f51f77646a4846', last_name='Рузанов', first_name='Евгений', middle_name='Фёдорович', role=user_role)
    Aluhug_user = User(login='Aluhug', password_hash='scrypt:32768:8:1$KTLSDQzX7bmMsfZT$aa2facfe0db6c07ccf67cbe5942befc134c8d733f84d8e29153ff9405643a87fc5ba7a682307dfc9303d8a10942dbc7e745c864386e99a30641aa50927b42fae', last_name='Алухугов', first_name='Алухуг', middle_name='Алухугович', role=user_role)

    db.session.add_all([kirillbad_user, BluePencilBoard_user, Jerold_user, Aluhug_user])
    db.session.commit() 

    fantasy = Style(style_name ="Фантастика")
    detective = Style(style_name ="Детектив")
    thriller = Style(style_name ="Триллер")
    db.session.add_all([fantasy, detective, thriller])
    db.session.commit() 