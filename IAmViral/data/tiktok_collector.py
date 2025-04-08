from TikTokApi import TikTokApi
import pandas as pd
from datetime import datetime
import os
import json

class TikTokCollector:
    def __init__(self):
        self.api = TikTokApi()
        # Configurar credenciales si están disponibles
        if os.getenv('TIKTOK_SESSION_ID'):
            self.api._session_id = os.getenv('TIKTOK_SESSION_ID')
        if os.getenv('TIKTOK_DEVICE_ID'):
            self.api._device_id = os.getenv('TIKTOK_DEVICE_ID')

    def collect_hashtag_videos(self, hashtag, limit=30):
        try:
            videos = []
            for video in self.api.hashtag(hashtag).videos(count=limit):
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
                    },
                    'url': f"https://www.tiktok.com/@{video_data['author']['uniqueId']}/video/{video_data['id']}"
                })
            return pd.DataFrame(videos)
        except Exception as e:
            print(f"Error recolectando datos de TikTok: {str(e)}")
            return pd.DataFrame()

    def collect_user_videos(self, username, limit=30):
        try:
            videos = []
            user = self.api.user(username)
            for video in user.videos(count=limit):
                video_data = video.as_dict
                videos.append({
                    'id': video_data['id'],
                    'desc': video_data['desc'],
                    'create_time': datetime.fromtimestamp(video_data['createTime']),
                    'music': video_data['music']['title'],
                    'stats': {
                        'digg_count': video_data['stats']['diggCount'],
                        'share_count': video_data['stats']['shareCount'],
                        'comment_count': video_data['stats']['commentCount'],
                        'play_count': video_data['stats']['playCount']
                    },
                    'url': f"https://www.tiktok.com/@{username}/video/{video_data['id']}"
                })
            return pd.DataFrame(videos)
        except Exception as e:
            print(f"Error recolectando videos del usuario: {str(e)}")
            return pd.DataFrame()

    def save_data(self, data, filename):
        try:
            if isinstance(data, pd.DataFrame):
                data.to_csv(f'data/tiktok/{filename}.csv', index=False)
            else:
                with open(f'data/tiktok/{filename}.json', 'w') as f:
                    json.dump(data, f)
            print(f"Datos de TikTok guardados en {filename}")
        except Exception as e:
            print(f"Error guardando datos de TikTok: {str(e)}")

if __name__ == '__main__':
    collector = TikTokCollector()
    
    # Ejemplo de recolección de datos
    hashtag_videos = collector.collect_hashtag_videos('viral')
    user_videos = collector.collect_user_videos('ejemplo_usuario')
    
    collector.save_data(hashtag_videos, 'tiktok_hashtag_data')
    collector.save_data(user_videos, 'tiktok_user_data') 