# coding=utf-8
# 建立資料表欄位
from app import db
import json

tags = db.Table('product_tags_mapping',
                db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
                )


class Product(db.Model):
    __table__name = '"product"'
    # 設定 primary_key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship('Brand', foreign_keys=[brand_id], uselist=False)
    category_depth_1_tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    category_depth_2_tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    category_depth_3_tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    category_depth_1_tag = db.relationship('Tag', foreign_keys=[category_depth_1_tag_id], uselist=False)
    category_depth_2_tag = db.relationship('Tag', foreign_keys=[category_depth_2_tag_id], uselist=False)
    category_depth_3_tag = db.relationship('Tag', foreign_keys=[category_depth_3_tag_id], uselist=False)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery')
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    series = db.relationship('Series', foreign_keys=[series_id], uselist=False)
    price = db.Column(db.Integer, nullable=False)
    volume = db.Column(db.String(10), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    reviews = db.relationship('Review', lazy=True, backref='product')

    def __init__(self, id, name, brand, category_depth_1_tag, category_depth_2_tag, category_depth_3_tag,
                 series, price, volume, release_date, tags=[]
                 , reviews=[]
                 ):
        self.id = id
        self.name = name
        self.brand = brand
        self.category_depth_1_tag = category_depth_1_tag
        self.category_depth_2_tag = category_depth_2_tag
        self.category_depth_3_tag = category_depth_3_tag
        self.tags = tags
        self.series = series
        self.price = price
        self.volume = volume
        self.release_date = release_date
        self.reviews = reviews

    def __repr__(self):
        return json.dumps(self)
