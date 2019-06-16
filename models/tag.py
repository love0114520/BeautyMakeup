# coding=utf-8
# 建立資料表欄位
from app import db
import json


class Tag(db.Model):
    __table__name = '"tag"'
    # 設定 primary_key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return json.dumps(self)
