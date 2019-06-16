# coding=utf-8
import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://appUser:pa$$word1234@localhost:5432/makeup'
db = SQLAlchemy(app)


@app.route('/')
def index():
    from models.brand import Brand
    from models.tag import Tag
    from models.series import Series
    from models.product import Product
    from models.review import Review


    # product = Product(id=1, name='雪肌粹', brand=Brand(1, 'Foo', 123456), category_depth_1_tag=Tag(1, '1'),
    #                   category_depth_2_tag=Tag(2, '22'), category_depth_3_tag=Tag(3, '333'),
    #                   tags=[Tag(4, '臉部保養'), Tag(5, '面膜'), Tag(6, '泥膜')],
    #                   series=Series(1, 'Bar'), price=987, volume='10.9 ml', release_date=datetime.datetime.now())
    # review = Review(id=1, user_skin='', user_age=99, publish_date=datetime.datetime.now(), content='This is the fucking cosmetic product review.', product_id=product.id)
    # db.session.merge(product)
    # db.session.merge(review)

    return render_template('index.html')


@app.route('/review_counts_ranking', methods=['GET'])
def review_counts_ranking():
    date_format = '%Y-%m-%d'
    now = datetime.datetime.now()
    time_delta = datetime.timedelta(days=-365)
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)
    start_date = datetime.datetime.strptime(start_date, date_format) if start_date is not None else now + time_delta
    end_date = datetime.datetime.strptime(end_date, date_format) if end_date is not None else now

    result = db.session.execute(
        """
        select b.name as brand_name, p.name as product_name, p.price, p.volume, p.release_date, t.review_count
        from  (
            select r.product_id, count(*) as review_count
            from "review" r
            where
            r.publish_date between DATE :start_date and DATE :end_date
            group by r.product_id
            order by review_count desc
        ) t
        join "product" p on t.product_id = p.id
        join "brand" b on p.brand_id = b.id
        order by t.review_count desc
        """, {
            'start_date': start_date,
            'end_date': end_date
        })
    results = [r for r in result.fetchall()]
    return render_template('review_counts_ranking.html', start_date=start_date.strftime(date_format), end_date=end_date.strftime(date_format), results=results)


@app.route('/tag_frequency_in_review_ranking')
def tag_frequency_in_review_ranking():
    from models.brand import Brand
    from models.product import Product
    from models.review import Review
    from models.series import Series
    from models.tag import Tag
    review_count = request.args.get('review_count', 100)
    brand_id = request.args.get('brand_id', None)
    product_id = request.args.get('product_id', None)
    if brand_id == '-1':
        brand_id = None
    if product_id == '-1':
        product_id = None
    brands = db.session.query(Brand).filter(Brand.products.any()).all()
    result = db.session.execute(
        """
        select b.name as brand_name,p.name as product_name, p.price, p.volume,g.name as tag_name,t.tag_in_reviews,t2.review_count, CAST (t.tag_in_reviews AS FLOAT) / t2.review_count as ratio
        from (
            select p.id as product_id, t.id as tag_id, count(*) as tag_in_reviews
            from "product_tags_mapping" m
            join "product" p on m.product_id = p.id
            join "tag" t on m.tag_id = t.id
            join "review" r on r.product_id = p.id
            where
            r.content like '%'||t.name||'%'""" +
        (""" and p.brand_id = :brand_id""" if brand_id is not None else """""") +
        (""" and p.id = :product_id""" if product_id is not None else """""") +
        """
            group by p.id, t.id
        ) t
        join (
            select p.id as product_id, count(*) as review_count
            from "product" p
            join "review" r on r.product_id = p.id""" +
        (""" and p.brand_id = :brand_id""" if brand_id is not None else """""") +
        (""" and p.id = :product_id""" if product_id is not None else """""") +
        """
            group by p.id
        ) t2 on t.product_id = t2.product_id
        join "product" p on t.product_id = p.id
        join "tag" g on t.tag_id = g.id
        join "brand" b on p.brand_id = b.id
        where
        t2.review_count >= :review_count
        order by ratio desc
        """, {'review_count': review_count, 'brand_id': brand_id, 'product_id': product_id})
    results = [r for r in result.fetchall()]
    return render_template('tag_frequency_in_review_ranking.html', review_count=review_count, brands=brands, brand_id=brand_id if brand_id is not None else '-1', product_id=product_id if product_id is not None else '-1', results=results)


if __name__ == '__main__':
    app.run()
