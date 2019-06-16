# coding=utf-8
# 建立資料表欄位
from app import db
import json


class Brand(db.Model):
    __table__name = '"brand"'
    # 設定 primary_key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    follow_number = db.Column(db.Integer)
    products = db.relationship('Product')

    def __init__(self, id, name, follow_number):
        self.id = id
        self.name = name
        self.follow_number = follow_number

    def __repr__(self):
        return json.dumps(self)
