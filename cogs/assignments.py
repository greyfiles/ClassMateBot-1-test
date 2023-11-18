# Copyright (c) 2023 nfoster1492
# This functionality provides various methods to manage assignments
# The isntructor is able to add/edit/and delete assignments
# and specify their grading category and point value.
import os
import sys
import discord
from discord.ext import commands

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import db


class Assignments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -----------------------------------------------------------------------------------------------------------------
    #    Function: add_assignment(self, ctx, assignmentname, categoryname, points)
    #    Description: This command lets the instructor add a new gradeable assignment
    #    Inputs:
    #    - self: used to access parameters passed to the class through the constructor
    #    - ctx: used to access the values passed through the current context
    #    - assignmentname: the name of the assignment
    #    - categoryname: the name of the grade category if the assignment
    #    - points: the points that the assignment is worth
    #    Outputs: Whether or not the add was a success
    # -----------------------------------------------------------------------------------------------------------------
    @commands.has_role("Instructor")
    @commands.command(
        name="addassignment",
        help="add a grading assignment and points $addassignment NAME CATEGORY POINTS",
    )
    async def add_assignment(
        self, ctx, assignmentname: str, categoryname: str, points: str
    ):
        """Add a grading assignment and points"""
        try:
            assignmentpoints = int(points)
        except ValueError:
            await ctx.send("Points could not be parsed")
            return
        category = db.query(
            "SELECT id FROM grade_categories WHERE guild_id = %s AND category_name = %s",
            (ctx.guild.id, categoryname),
        )

        if not category:
            await ctx.send(f"Category with name {categoryname} does not exist")
            return
        if assignmentpoints < 0:
            await ctx.send("Assignment points must be greater than or equal to zero")
            return
        existing = db.query(
            "SELECT id FROM assignments WHERE guild_id = %s AND assignment_name = %s",
            (ctx.guild.id, assignmentname),
        )

        if not existing:
            db.query(
                "INSERT INTO assignments (guild_id, category_id, assignment_name, points) VALUES (%s, %s, %s, %s)",
                (ctx.guild.id, category[0], assignmentname, points),
            )
            await ctx.send(
                f"A grading assignment has been added for: {assignmentname}  with points: {points} and category: {categoryname}"
            )
        else:
            await ctx.send("This assignment has already been added..!!")

    # -----------------------------------------------------------------------------------------------------------------
    #    Function: edit_assignment(self, ctx, assignmentname, categoryname, points)
    #    Description: This command lets the instructor edit a gradeable assignment with a new categoryname and/or points
    #    Inputs:
    #    - self: used to access parameters passed to the class through the constructor
    #    - ctx: used to access the values passed through the current context
    #    - assignmentname: the name of the assignment
    #    - categoryname: the new name of the grade category if the assignment
    #    - points: the new points that the assignment is worth
    #    Outputs: Whether or not the edit was a success
    # -----------------------------------------------------------------------------------------------------------------
    @commands.has_role("Instructor")
    @commands.command(
        name="editassignment",
        help="edit a grading assignment and points $editassignment NAME CATEGORY POINTS",
    )
    async def edit_assignment(
        self, ctx, assignmentname: str, categoryname: str, points: str
    ):
        """edit a grading assignment and points $editassignment NAME CATEGORY POINTS"""
        try:
            assignmentpoints = int(points)
        except ValueError:
            await ctx.send("Points could not be parsed")
            return
        category = db.query(
            "SELECT id FROM grade_categories WHERE guild_id = %s AND category_name = %s",
            (ctx.guild.id, categoryname),
        )
        if not category:
            await ctx.send(f"Category with name {categoryname} does not exist")
            return
        if assignmentpoints < 0:
            await ctx.send("Assignment points must be greater than or equal to zero")
            return
        existing = db.query(
            "SELECT id FROM assignments WHERE guild_id = %s AND assignment_name = %s",
            (ctx.guild.id, assignmentname),
        )
        if existing:
            db.query(
                "UPDATE assignments SET category_id = %s, points = %s WHERE id = %s",
                (category[0], points, existing[0]),
            )
            await ctx.send(
                f"{assignmentname} assignment has been updated with points:{points} and category: {categoryname}"
            )
        else:
            await ctx.send("This assignment does not exist")

    # -----------------------------------------------------------------------------------------------------------------
    #    Function: delete_assignment(self, ctx, assignmentname)
    #    Description: This command lets the instructor delete a gradeable assignment
    #    Inputs:
    #    - self: used to access parameters passed to the class through the constructor
    #    - ctx: used to access the values passed through the current context
    #    - assignmentname: the name of the assignment
    #    Outputs: Whether or not the delete was a success
    # -----------------------------------------------------------------------------------------------------------------
    @commands.has_role("Instructor")
    @commands.command(
        name="deleteassignment",
        help="delete a grading assignment $deleteassignment NAME",
    )
    async def delete_assignment(self, ctx, assignmentname: str):
        """delete a grading assignment $deleteassignment NAME"""
        existing = db.query(
            "SELECT id FROM assignments WHERE guild_id = %s AND assignment_name = %s",
            (ctx.guild.id, assignmentname),
        )
        if existing:
            db.query("DELETE FROM assignments WHERE id = %s", (existing[0]))
            await ctx.send(f"{assignmentname} assignment has been deleted ")
        else:
            await ctx.send("This assignment does not exist")

    # -----------------------------------------------------------------------------------------------------------------
    #    Function: add_assignment_error(self, ctx, error)
    #    Description: prints error message for addassignment command
    #    Inputs:
    #       - ctx: context of the command
    #       - error: error message
    #    Outputs:
    #       - Error details
    # -----------------------------------------------------------------------------------------------------------------
    @add_assignment.error
    async def add_assignment_error(self, ctx, error):
        """Error handling of addassignment function"""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "To use the addassignment command, do: $addassignment <assignmentname> <categoryname> <points> \n ( For example: $addassignment test1 tests 100 )"
            )
            await ctx.message.delete()
        else:
            await ctx.author.send(error)
            print(error)

    # -----------------------------------------------------------------------------------------------------------------
    #    Function: edit_assignment_error(self, ctx, error)
    #    Description: prints error message for editassignment command
    #    Inputs:
    #       - ctx: context of the command
    #       - error: error message
    #    Outputs:
    #       - Error details
    # -----------------------------------------------------------------------------------------------------------------
    @edit_assignment.error
    async def edit_assignment_error(self, ctx, error):
        """Error handling of editassignment function"""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "To use the editassignment command, do: $editassignment <assignmentname> <categoryname> <points> \n ( For example: $editassignment test1 tests 95 )"
            )
            await ctx.message.delete()
        else:
            await ctx.author.send(error)
            print(error)

    # -----------------------------------------------------------------------------------------------------------------
    #    Function: delete_assignment_error(self, ctx, error)
    #    Description: prints error message for deleteassignment command
    #    Inputs:
    #       - ctx: context of the command
    #       - error: error message
    #    Outputs:
    #       - Error details
    # -----------------------------------------------------------------------------------------------------------------
    @delete_assignment.error
    async def delete_assignment_error(self, ctx, error):
        """Error handling of deleteassignment function"""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "To use the deleteassignment command, do: $deleteassignment <assignmentname>\n ( For example: $deleteassignment test1)"
            )
            await ctx.message.delete()
        else:
            await ctx.author.send(error)
            print(error)


# -------------------------------------
# add the file to the bot's cog system
# -------------------------------------
async def setup(bot):
    """Adds the file to the bot's cog system"""
    await bot.add_cog(Assignments(bot))
