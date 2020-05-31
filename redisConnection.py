import pyarrow as pa
import pandas as pd
import redis
import dotenv
import os

dotenv.load_dotenv()


class RedisConnection:

    def __init__(self):
        print("PID %d: initializing redis pool..." % os.getpid())
        self.redis_pool = redis.ConnectionPool(host=os.environ.get('REDIS_HOST'),
                                               port=os.environ.get('REDIS_PORT'),
                                               db=os.environ.get('REDIS_DB'))

    def cache_df(self, alias, df):
        cur = redis.Redis(connection_pool=self.redis_pool)
        context = pa.default_serialization_context()
        df_compressed = context.serialize(df).to_buffer().to_pybytes()

        res = cur.set(alias, df_compressed)
        if res == True:
            print('df cached')

    def get_cached_df(self, alias):

        cur = redis.Redis(connection_pool=self.redis_pool)
        context = pa.default_serialization_context()
        all_keys = [key.decode("utf-8") for key in cur.keys()]

        if alias in all_keys:
            result = cur.get(alias)

            dataframe = pd.DataFrame.from_dict(context.deserialize(result))

            # Copy makes sure the object is editable, not necessary if all transformations are done beforehand
            return dataframe.copy()

        return None

    def get_cached_json(self, alias):

        cur = redis.Redis(connection_pool=self.redis_pool)
        context = pa.default_serialization_context()
        all_keys = [key.decode("utf-8") for key in cur.keys()]

        if alias in all_keys:
            result = cur.get(alias)

            json_result = context.deserialize(result)

            return json_result

        return None


