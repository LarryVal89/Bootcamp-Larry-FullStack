import instaloader
import pandas as pd
from datetime import datetime
import os
import json

class InstagramCollector:
    def __init__(self):
        self.loader = instaloader.Instaloader()
        # Iniciar sesión si es necesario
        if os.getenv('INSTAGRAM_USERNAME') and os.getenv('INSTAGRAM_PASSWORD'):
            self.loader.login(
                os.getenv('INSTAGRAM_USERNAME'),
                os.getenv('INSTAGRAM_PASSWORD')
            )

    def collect_hashtag_posts(self, hashtag, limit=30):
        try:
            posts = []
            hashtag_posts = instaloader.Hashtag.from_name(self.loader.context, hashtag)
            
            for post in hashtag_posts.get_top_posts():
                if len(posts) >= limit:
                    break
                    
                posts.append({
                    'id': post.mediaid,
                    'shortcode': post.shortcode,
                    'caption': post.caption,
                    'likes': post.likes,
                    'comments': post.comments,
                    'timestamp': post.date_local,
                    'is_video': post.is_video,
                    'video_view_count': post.video_view_count if post.is_video else 0,
                    'owner': post.owner_username,
                    'url': f"https://www.instagram.com/p/{post.shortcode}/"
                })
                
            return pd.DataFrame(posts)
        except Exception as e:
            print(f"Error recolectando datos de Instagram: {str(e)}")
            return pd.DataFrame()

    def collect_user_posts(self, username, limit=30):
        try:
            posts = []
            profile = instaloader.Profile.from_username(self.loader.context, username)
            
            for post in profile.get_posts():
                if len(posts) >= limit:
                    break
                    
                posts.append({
                    'id': post.mediaid,
                    'shortcode': post.shortcode,
                    'caption': post.caption,
                    'likes': post.likes,
                    'comments': post.comments,
                    'timestamp': post.date_local,
                    'is_video': post.is_video,
                    'video_view_count': post.video_view_count if post.is_video else 0,
                    'url': f"https://www.instagram.com/p/{post.shortcode}/"
                })
                
            return pd.DataFrame(posts)
        except Exception as e:
            print(f"Error recolectando posts del usuario: {str(e)}")
            return pd.DataFrame()

    def save_data(self, data, filename):
        try:
            if isinstance(data, pd.DataFrame):
                data.to_csv(f'data/instagram/{filename}.csv', index=False)
            else:
                with open(f'data/instagram/{filename}.json', 'w') as f:
                    json.dump(data, f)
            print(f"Datos de Instagram guardados en {filename}")
        except Exception as e:
            print(f"Error guardando datos de Instagram: {str(e)}")

if __name__ == '__main__':
    collector = InstagramCollector()
    
    # Ejemplo de recolección de datos
    hashtag_posts = collector.collect_hashtag_posts('viral')
    user_posts = collector.collect_user_posts('ejemplo_usuario')
    
    collector.save_data(hashtag_posts, 'instagram_hashtag_data')
    collector.save_data(user_posts, 'instagram_user_data') 