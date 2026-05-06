from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Teams
        marvel = Team.objects.create(name='marvel', description='Marvel Team')
        dc = Team.objects.create(name='dc', description='DC Team')

        # Users
        users = [
            User(email='tony@stark.com', name='Tony Stark', team='marvel'),
            User(email='steve@rogers.com', name='Steve Rogers', team='marvel'),
            User(email='bruce@wayne.com', name='Bruce Wayne', team='dc'),
            User(email='clark@kent.com', name='Clark Kent', team='dc'),
        ]
        User.objects.bulk_create(users)

        # Activities
        Activity.objects.create(user='tony@stark.com', type='run', duration=30, date='2023-01-01')
        Activity.objects.create(user='steve@rogers.com', type='swim', duration=45, date='2023-01-02')
        Activity.objects.create(user='bruce@wayne.com', type='cycle', duration=60, date='2023-01-03')
        Activity.objects.create(user='clark@kent.com', type='fly', duration=120, date='2023-01-04')

        # Leaderboard
        Leaderboard.objects.create(team='marvel', points=200)
        Leaderboard.objects.create(team='dc', points=180)

        # Workouts
        Workout.objects.create(name='Pushups', description='Do 20 pushups', difficulty='easy')
        Workout.objects.create(name='Flight', description='Fly for 10 minutes', difficulty='hard')

        # Ensure unique index on email (users)
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        db.users.create_index([('email', 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('Database populated with test data.'))
