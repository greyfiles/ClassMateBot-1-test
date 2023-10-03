import os
import sys
import discord
from discord.ext import commands
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import db

class Grades(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="categories", help="display all grading categories and weights $categories")
    async def categories(self, ctx):

        categories = db.query(
            'SELECT category_name, category_weight FROM grade_categories WHERE guild_id = %s ORDER BY category_weight DESC',
            (ctx.guild.id,)
        )


        await ctx.send("Category | Weight")
        await ctx.send("================")

        for category_name, category_weight in categories:
            await ctx.send(f"{category_name} | {category_weight}")
        
    @commands.command(name="addgradecategory", help="add a grading category and weight $addgradecategory NAME WEIGHT")
    async def add_grade_category(self, ctx, categoryname: str, weight: str):
        try:
            categoryweight = float(weight)
        except ValueError:
            await ctx.send("Weight could not be parsed")
            return
        existing = db.query(
            'SELECT id FROM grade_categories WHERE guild_id = %s AND category_name = %s',
            (ctx.guild.id, categoryname)
        )
        if not existing:
            db.query(
                'INSERT INTO grade_categories (guild_id, category_name, category_weight) VALUES (%s, %s, %s)',
                (ctx.guild.id, categoryname, weight)
            )
            await ctx.send(
                f"A grading category has been added for: {categoryname}  with weight: {weight} ")
        else:
            await ctx.send("This category has already been added..!!")


    @commands.command(name="editgradecategory", help="edit a grading category and weight $editgradecategory NAME WEIGHT")
    async def edit_grade_category(self, ctx, categoryname: str, weight: str):
        try:
            categoryweight = float(weight)
        except ValueError:
            await ctx.send("Weight could not be parsed")
            return
        existing = db.query(
            'SELECT id FROM grade_categories WHERE guild_id = %s AND category_name = %s',
            (ctx.guild.id, categoryname)
        )
        if existing:
            db.query(
                'UPDATE grade_categories SET category_weight = %s WHERE id = %s',
                (weight, existing[0])
            )
            await ctx.send(
                f"{categoryname} category has been updated with weight:{weight} ")
        else:
            await ctx.send("This category does not exist")

    @commands.command(name="deletegradecategory", help="delete a grading category $deletegradecategory NAME")
    async def delete_grade_category(self, ctx, categoryname: str):
        existing = db.query(
            'SELECT id FROM grade_categories WHERE guild_id = %s AND category_name = %s',
            (ctx.guild.id, categoryname)
        )
        if existing:
            db.query(
                'DELETE FROM grade_categories WHERE id = %s',
                (existing[0])
            )
            await ctx.send(
                f"{categoryname} category has been deleted ")
        else:
            await ctx.send("This category does not exist")
    
    @add_grade_category.error
    async def add_grade_category_error(self, ctx, error):
        await ctx.author.send(error)

    @edit_grade_category.error
    async def edit_grade_category_error(self, ctx, error):
        await ctx.author.send(error)
    
    @delete_grade_category.error
    async def delete_grade_category_error(self, ctx, error):
        await ctx.author.send(error)

async def setup(bot):
    await bot.add_cog(Grades(bot))