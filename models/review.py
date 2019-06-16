# coding=utf-8
# 建立資料表欄位
from app import db
import json


class Review(db.Model):
    __table__name = '"review"'
    # 設定 primary_key
    id = db.Column(db.Integer, primary_key=True)
    user_skin = db.Column(db.String(256), nullable=False)
    user_age = db.Column(db.Integer, nullable=False)
    publish_date = db.Column(db.DateTime, nullable=False)
    update_date = db.Column(db.DateTime, nullable=True)
    content = db.Column(db.UnicodeText, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __init__(self, id, user_skin, user_age, publish_date, content
                 , product_id
                 , update_date=None):
        self.id = id
        self.user_skin = user_skin
        self.user_age = user_age
        self.publish_date = publish_date
        self.update_date = update_date
        self.content = content
        self.product_id = product_id

    def __repr__(self):
        return json.dumps(self)
