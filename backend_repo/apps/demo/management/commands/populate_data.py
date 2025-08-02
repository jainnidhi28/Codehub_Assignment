from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.demo.models import Post, Comment
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate database with sample posts and comments'

    def handle(self, *args, **options):
        # Create a test user if it doesn't exist
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Created user: {user.username}')
            )
        
        # Sample post texts
        post_texts = [
            "Just watched an amazing movie! The special effects were incredible.",
            "Can't believe how good this film was. Highly recommend!",
            "The character development in this movie is outstanding.",
            "This is definitely going in my top 10 list.",
            "The soundtrack was absolutely perfect for this film.",
            "I love how they handled the story arc in this movie.",
            "The cinematography in this film is breathtaking.",
            "This movie exceeded all my expectations!",
            "The acting performances were phenomenal.",
            "I can't wait to watch this again with friends.",
            "The plot twists in this movie were unexpected and brilliant.",
            "This film has such a great message.",
            "The visual effects team did an incredible job.",
            "I'm still thinking about this movie days later.",
            "This is a masterpiece of modern cinema."
        ]
        
        # Sample comment texts
        comment_texts = [
            "I completely agree!",
            "Great review, thanks for sharing.",
            "I had the same thoughts about this movie.",
            "You've convinced me to watch it!",
            "The soundtrack really was amazing.",
            "I loved that scene too!",
            "Thanks for the recommendation!",
            "I can't wait to see it now.",
            "You captured my thoughts exactly.",
            "I'm going to watch it this weekend.",
            "The special effects were mind-blowing.",
            "I agree about the character development.",
            "This movie deserves all the awards.",
            "I'm so glad I watched this!",
            "The ending was perfect."
        ]
        
        # Create posts
        posts_created = 0
        for i, text in enumerate(post_texts):
            # Create post with timestamp going backwards (newest first)
            timestamp = datetime.now() - timedelta(hours=i)
            post = Post.objects.create(
                text=text,
                user=user,
                timestamp=timestamp
            )
            
            # Add 3-7 comments to each post
            num_comments = random.randint(3, 7)
            for j in range(num_comments):
                comment_text = random.choice(comment_texts)
                comment_timestamp = timestamp + timedelta(minutes=j+1)
                Comment.objects.create(
                    text=comment_text,
                    post=post,
                    user=user,
                    timestamp=comment_timestamp
                )
            
            posts_created += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {posts_created} posts with comments'
            )
        )
        
        # Show some statistics
        total_posts = Post.objects.count()
        total_comments = Comment.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Database now contains: {total_posts} posts, {total_comments} comments'
            )
        ) 