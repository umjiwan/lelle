import sqlite3
import datetime
from discord.ext import commands

class d_day:
    def __init__(self):
        self.connect = sqlite3.connect("../data/lelle.db")
        self.cursor = self.connect.cursor()
        self.cursor.execute("\
                CREATE TABLE IF NOT EXISTS dday (\
                userid text PRIMARY KEY,\
                now text,\
                day text)")
        self.connect.commit()
        self.today = datetime.datetime.now()
    
    def save_d_day(self, user_id: str, day: str):
        self.cursor.execute(f"""
            SELECT day FROM dday WHERE userid = "{user_id}"        
        """)

        result = self.cursor.fetchone()

        if not result:
            self.cursor.execute(f"INSERT INTO dday VALUES(\
                                '{user_id}',\
                                '{self.today}',\
                                '{day}')")

        else:
            self.cursor.execute(f"UPDATE dday SET day = '{day}' WHERE userid='{user_id}'")
        
        self.connect.commit()

    def delete_d_day(self, user_id: str):
        self.cursor.execute(f"DELETE FROM dday WHERE userid='{user_id}'")
        self.connect.commit()

    def view_d_day(self, user_id: str):
        self.cursor.execute(f"SELECT now, day FROM dday WHERE userid='{user_id}'")
        result = self.cursor.fetchone()

        if not result:
            return None
        else:
            day = result[1].split("-")
            day = datetime.datetime(int(day[0]), int(day[1]), int(day[2]))
            d_day = str((self.today - day).days + 1)

            if d_day[0] != "-":
                d_day = "+" + d_day
            
            return d_day

    def close_database(self):
        self.connect.close()

class Core(commands.Cog):
    def __init__(self, lelle):
        self.lelle = lelle
    
    @commands.command(aliases=["디데이"])
    async def d_day(self, ctx, *, sentence: str):
        user_id = str(ctx.author.id)
        command = sentence.split(" ")[0]
        day = sentence.split(" ")[1] if len(sentence.split(" ")) != 1 else "0-0-0"

        dd = d_day()
        if command == "등록":
            dd.save_d_day(user_id, day)
        elif command == "삭제":
            dd.delete_d_day(user_id)
        dd.close_database()
        await ctx.channel.send(f"디데이가 {command}되었습니다!")

def setup(lelle):
    lelle.add_cog(Core(lelle))

        
if __name__ == "__main__":
    dd = d_day()
    dd.save_d_day("test", "2022-01-01")
    day = dd.view_d_day("test")
    dd.close_database()

    print(day)
