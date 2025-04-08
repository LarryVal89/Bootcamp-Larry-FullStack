import tweepy
from pytrends.request import TrendReq
from TikTokApi import TikTokApi
import pandas as pd
import json
from datetime import datetime, timedelta
import os

class DataCollector:
    def __init__(self):
        # Inicializar APIs (requiere tokens reales)
        self.twitter_auth = tweepy.OAuthHandler(
            os.getenv('TWITTER_API_KEY'),
            os.getenv('TWITTER_API_SECRET')
        )
        self.twitter_auth.set_access_token(
            os.getenv('TWITTER_ACCESS_TOKEN'),
            os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )
        self.twitter_api = tweepy.API(self.twitter_auth)
        self.pytrends = TrendReq()
        
        # Inicializar TikTok API
        self.tiktok_api = TikTokApi()

    def collect_twitter_data(self, hashtag, limit=100):
        try:
            tweets = []
            for tweet in tweepy.Cursor(
                self.twitter_api.search_tweets,
                q=hashtag,
                lang="es",
                tweet_mode='extended'
            ).items(limit):
                tweets.append({
                    'text': tweet.full_text,
                    'retweets': tweet.retweet_count,
                    'likes': tweet.favorite_count,
                    'created_at': tweet.created_at
                })
            return pd.DataFrame(tweets)
        except Exception as e:
            print(f"Error recolectando datos de Twitter: {str(e)}")
            return pd.DataFrame()

    def collect_google_trends(self, keyword, timeframe='today 3-m'):
        try:
            self.pytrends.build_payload([keyword], timeframe=timeframe)
            interest_over_time = self.pytrends.interest_over_time()
            return interest_over_time
        except Exception as e:
            print(f"Error recolectando datos de Google Trends: {str(e)}")
            return pd.DataFrame()

    def collect_tiktok_data(self, hashtag, limit=30):
        try:
            videos = []
            for video in self.tiktok_api.hashtag(hashtag).videos(count=limit):
                video_data = video.as_dict
                videos.append({
                    'id': video_data['id'],
                    'desc': video_data['desc'],
                    'create_time': datetime.fromtimestamp(video_data['createTime']),
                    'author': video_data['author']['uniqueId'],
                    'music': video_data['music']['title'],
                    'stats': {
                        'digg_count': video_data['stats']['diggCount'],
                        'share_count': video_data['stats']['shareCount'],
                        'comment_count': video_data['stats']['commentCount'],
                        'play_count': video_data['stats']['playCount']
                    }
                })
            return pd.DataFrame(videos)
        except Exception as e:
            print(f"Error recolectando datos de TikTok: {str(e)}")
            return pd.DataFrame()

    def save_data(self, data, filename):
        try:
            if isinstance(data, pd.DataFrame):
                data.to_csv(f'data/{filename}.csv', index=False)
            else:
                with open(f'data/{filename}.json', 'w') as f:
                    json.dump(data, f)
            print(f"Datos guardados en {filename}")
        except Exception as e:
            print(f"Error guardando datos: {str(e)}")

if __name__ == '__main__':
    collector = DataCollector()
    
    # Ejemplo de recolección de datos
    twitter_data = collector.collect_twitter_data('#viral')
    google_data = collector.collect_google_trends('viral content')
    tiktok_data = collector.collect_tiktok_data('viral')
    
    collector.save_data(twitter_data, 'twitter_viral_data')
    collector.save_data(google_data, 'google_trends_data')
    collector.save_data(tiktok_data, 'tiktok_viral_data') 