import sqlite3

db_name = "itam.db"


def assign_laptops(db_name):
    """Assigns laptops to users and updates both tables."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # 1. Get all users and laptops
        cursor.execute("SELECT userid FROM users")
        users = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT hostname FROM laptops")
        laptops = [row[0] for row in cursor.fetchall()]

        # 2. Check if there are enough laptops for all users
        if len(laptops) < len(users):
            raise ValueError("Not enough laptops to assign to all users.")

        # 3. Assign laptops to users (you can use different assignment logic here)
        assignments = {}
        for i, user in enumerate(users):
            assignments[user] = laptops[i % len(laptops)] # Cycle through laptops if there are fewer laptops than users

        # 4. Update the 'users' table
        for user, laptop in assignments.items():
            cursor.execute("UPDATE users SET hostname = ? WHERE userid = ?", (laptop, user))

        # 5. Update the 'laptops' table
        for user, laptop in assignments.items():
            cursor.execute("UPDATE laptops SET assigned_user = ? WHERE hostname = ?", (user, laptop))

        conn.commit()  # Important: Commit the changes to the database
        print("Laptops assigned and tables updated successfully.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()  # Rollback changes in case of error
    except ValueError as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    db_name = "itam.db"
    assign_laptops(db_name)