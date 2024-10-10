import os
import msvcrt
from django.http import JsonResponse
from ..models import comments
import csv
from ..RestaurantLeaderboard import Leaderboard
from celery import shared_task
@shared_task
def export_comments_to_csv(res_id):
    data = comments.objects.filter(restaurant_id=res_id).last()
    # Fetch comments for the given restaurant I
    fields = ['Review'] 
    # if not data.exists():
    #     return JsonResponse({"message": "No comments found for this restaurant."}, status=404)
    
    # Create a directory for each restaurant's CSV file
    path=f'backend\\model\\csv_files\\comment.csv'
    if os.path.exists(path):
          data = comments.objects.filter(restaurant_id=res_id).last()
          with open(path, 'w', newline='', encoding='utf-8') as csvfile:
            # Acquire the file lock
            msvcrt.locking(csvfile.fileno(), msvcrt.LK_LOCK, os.path.getsize(path))
            
            writer = csv.writer(csvfile)
        
            
            # Write the data rows
            
            writer.writerow([getattr(data, field) for field in fields])
            
            print(f"CSV file saved at {path}")
            
            # Release the file lock
            msvcrt.locking(csvfile.fileno(), msvcrt.LK_UNLCK, os.path.getsize(path))
    
          return True

    directory = f'backend\\model\\csv_files'
    os.makedirs(directory, exist_ok=True)
    
    # Define the path to the CSV file
    csv_file_path = os.path.join(directory, 'comments.csv')
    
    # Specify the fields you want to include in the CSV
    fields = ['Review']  # Adjust this to match your actual field names

    try:
        # Open the file for writing
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            # Acquire the file lock
            msvcrt.locking(csvfile.fileno(), msvcrt.LK_LOCK, os.path.getsize(csv_file_path))
            
            writer = csv.writer(csvfile)
            
            # Write the header
            writer.writerow(fields)
            
            # Write the data rows
        
            writer.writerow([getattr(data, field) for field in fields])
            
            print(f"CSV file saved at {csv_file_path}")
            
            # Release the file lock
            msvcrt.locking(csvfile.fileno(), msvcrt.LK_UNLCK, os.path.getsize(csv_file_path))
    
    except Exception as e:
        return False
    
    return True