from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///StudyCounter.db?check_same_thread=False', echo=True)

Base = declarative_base()

from sqlalchemy import Column, Integer, String, Float


from sqlalchemy.orm import sessionmaker

# engine是2.2中创建的连接
Session = sessionmaker(bind=engine)

# 创建Session类实例
session = Session()

class DayPlan(Base):
    # 指定本类映射到DayPlan表
    __tablename__ = 'DayPlan'
    
    # 各变量名一定要与表的各字段名一样，因为相同的名字是他们之间的唯一关联关系
    # 从语法上说，各变量类型和表的类型可以不完全一致，如表字段是String(64)，但我就定义成String(32)
    # 但为了避免造成不必要的错误，变量的类型和其对应的表的字段的类型还是要相一致
    # 指定id映射到id字段; id字段为整型，为主键
    id = Column(Integer, primary_key=True)
    # 指定name映射到name字段; name字段为字符串类形，
    bigItem = Column(String(20))
    littleItem = Column(String(32))
    time = Column(Float)

    # 这个感觉并不需要写，但官方示例中有，也就根着模仿了，暂时没看到有什么用
    def __repr__(self):
        return "<DayPlan(bigItem='%s', littleItem='%s', time='%s')>" % (
                   self.bigItem, self.littleItem, self.time)


# 定义映射类User，其继承上一步创建的Base
class User(Base):
    # 指定本类映射到users表
    __tablename__ = 'users'
    
    # 各变量名一定要与表的各字段名一样，因为相同的名字是他们之间的唯一关联关系
    # 从语法上说，各变量类型和表的类型可以不完全一致，如表字段是String(64)，但我就定义成String(32)
    # 但为了避免造成不必要的错误，变量的类型和其对应的表的字段的类型还是要相一致
    # 指定id映射到id字段; id字段为整型，为主键
    id = Column(Integer, primary_key=True)
    # 指定name映射到name字段; name字段为字符串类形，
    name = Column(String(20))
    fullname = Column(String(32))
    password = Column(String(32))

    # 这个感觉并不需要写，但官方示例中有，也就根着模仿了，暂时没看到有什么用
    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                   self.name, self.fullname, self.password)


# 查看映射对应的表
User.__table__

DayPlan.__table__

# 创建数据表。一方面通过engine来连接数据库，另一方面根据哪些类继承了Base来决定创建哪些表
# checkfirst=True，表示创建表前先检查该表是否存在，如同名表已存在则不再创建。其实默认就是True
Base.metadata.create_all(engine, checkfirst=True)

# 上边的写法会在engine对应的数据库中创建所有继承Base的类对应的表，但很多时候很多只是用来则试的或是其他库的
# 此时可以通过tables参数指定方式，指示仅创建哪些表
# Base.metadata.create_all(engine,tables=[Base.metadata.tables['users']],checkfirst=True)
# 在项目中由于model经常在别的文件定义，没主动加载时上边的写法可能写导致报错，可使用下边这种更明确的写法
# User.__table__.create(engine, checkfirst=True)

# 另外我们说这一步的作用是创建表，当我们已经确定表已经在数据库中存在时，我完可以跳过这一步
# 针对已存放有关键数据的表，或大家共用的表，直接不写这创建代码更让人心里踏实


###########################################################




# 创建User类实例
ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')

# 将该实例插入到users表
session.add(ed_user)

# 一次插入多条记录形式
session.add_all(
    [User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')]
)
# 当前更改只是在session中，需要使用commit确认更改才会写入数据库
session.commit()


# 创建DayPlan类实例
ed_dayPlan = DayPlan(bigItem='202', littleItem='PP refine', time=0.5)

# 将该实例插入到users表
session.add(ed_dayPlan)

# 一次插入多条记录形式
session.add_all(
    [DayPlan(bigItem='273', littleItem='review', time=1.1),
    DayPlan(bigItem='202', littleItem='PP refine', time=1.2),
    DayPlan(bigItem='273', littleItem='preview', time=1)]
)
# 当前更改只是在session中，需要使用commit确认更改才会写入数据库
session.commit()


###########################################################

# 指定User类查询users表，查找name为'ed'的第一条数据。有all()/one()/first()等
# 最后的all()之类的筛选词是必须的，不然并不会真的发起查询
our_user = session.query(User).filter_by(name='ed').first()
our_plan = session.query(DayPlan).filter_by(bigItem='202').first()
our_user
our_user
# 比较ed_user与查询到的our_user是否为同一条记录
ed_user is our_user
ed_dayPlan is our_plan
# 只获取指定字段
# 但要注意如果只获取部分字段，那么返回的就是元组而不是对象了
# session.query(User.name).filter_by(name='ed').all()
# like查询
# session.query(User).filter(User.name.like("ed%")).all()
# 正则查询
# session.query(User).filter(User.name.op("regexp")("^ed")).all()
# 统计数量
# session.query(User).filter(User.name.like("ed%")).count()
# 调用数据库内置函数
# 以count()为例，都是直接func.func_name()这种格式，func_name与数据库内的写法保持一致
# from sqlalchemy import func
# session.query(func.count(User3.name)).one()

########################################################################

# 要修改需要先将记录查出来
mod_user = session.query(User).filter_by(name='ed').first()

# 将ed用户的密码修改为modify_paswd
mod_user.password = 'modify_passwd'

# 确认修改
session.commit()

# 要修改需要先将记录查出来
mod_dayPlan = session.query(DayPlan).filter_by(bigItem='202').first()


mod_dayPlan.time = 10.01

# 确认修改
session.commit()

####################################################################

# 要删除需要先将记录查出来
del_user = session.query(User).filter_by(name='ed').first()

# 打印一下，确认未删除前记录存在
del_user

# 将ed用户记录删除
session.delete(del_user)

# 删除前得先查询，这写法似乎有点蠢，但是确实并没有原生的那种直接给条件然后删除的写法
# 类似一点的可以写成以下形式
# session.query(User).filter_by(name='ed').first().delete()

# 确认删除
session.commit()

# 遍历查看，已无ed用户记录
for user in session.query(User):
    print(user)


# 要删除需要先将记录查出来
del_dayPlan = session.query(DayPlan).filter_by(bigItem='202').first()

# 打印一下，确认未删除前记录存在
del_dayPlan

# 将ed用户记录删除
session.delete(del_dayPlan)

# 删除前得先查询，这写法似乎有点蠢，但是确实并没有原生的那种直接给条件然后删除的写法
# 类似一点的可以写成以下形式
# session.query(User).filter_by(name='ed').first().delete()

# 确认删除
session.commit()

# 遍历查看，已无ed用户记录
for dayPlan in session.query(DayPlan):
    print(dayPlan)