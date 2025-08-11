# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from wazzupScrap.models.models import Product, Productimages
from scrapy.pipelines.images import ImagesPipeline

class QuotescrapPipeline:
    # def __init__(self):

    def __init__(self, batch_size=100):

        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..','.env'))

        self.batch_size = batch_size
        self.items_buffer = []
        self.engine = create_engine(
            f"mysql+pymysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}/wassup_testing",
            echo=False  # Turn on True for debugging
        )
        self.session = None


    def open_spider(self, spider):
        # Create session once per spider run
        self.session = Session(self.engine)


    def process_item(self, item, spider):
        # Create ORM objects (not committed yet)
        product = Product(
            name=item['name'],
            price=item['price'],
            type="shirt",
            storeId=1000,
            productLink=item['productLink']
        )

        image = Productimages(
            URL=item['imageLink'],
            product=product
        )
        
        self.items_buffer.append((product, image))
        if len(self.items_buffer) >= self.batch_size:
            self.flush_to_db()
        
        return item
    
    
    def flush_to_db(self):
        for product, image in self.items_buffer:
            self.session.add(product)
            self.session.add(image)
        self.session.commit()
        self.items_buffer.clear()


    def close_spider(self, spider):
        # Commit remaining items in buffer
        if self.items_buffer:
            self.flush_to_db()
        self.session.close()
        
        
    def create_connection(self):
       
       engine = create_engine("mysql+pymysql://root:amreissa@localhost:3306/wassup_testing", echo=True)
       session = Session(engine)

    # def create_table(self):
    #     self.curr.execute("""DROP TABLE IF EXISTS product""")
    #     self.curr.execute("""create table shirts(
    #                       name text)""")



class MyImagesPipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        # results is a list of tuples (success, image_info)
        # image_info has 'path' key with downloaded image path relative to IMAGES_STORE
        image_paths = [x['path'] for ok, x in results if ok]
        if image_paths:
            # Store the first downloaded image path in your item
            item['imageLink'] = image_paths[0]
        else:
            item['imageLink'] = None
        return item