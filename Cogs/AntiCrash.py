import Config
import disnake
from disnake.ext import commands

class AntiCrash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def checkSuspiciousAction(self, deletedType, member, guildId):
        actionList = Config.deletedActions.get(guildId, {}).get(deletedType, {})

        try:
            if len(actionList.get(member.id, [])) < 3:
                return

            print("Анти-краш")
            del Config.deletedActions[guildId][deletedType][member.id]
            await member.ban(reason="Анти-краш система!")
        except:
            pass

    def addSuspiciousAction(self, deletedType, member, guildId):
        if not guildId in Config.deletedActions:
            Config.deletedActions[guildId] = {
                "users": {},
                "channels": {},
                "roles": {}
            }

        actionList = Config.deletedActions[guildId][deletedType]

        if not member.id in actionList:
            actionList[member.id] = [Config.timeSuspicion]
            return

        actionList[member.id].append(Config.timeSuspicion)

    async def checkAudit(self, action, target, actionType, guild):
        try:
            entry = await guild.audit_logs(
                limit=1, action=action
            ).find(lambda e: e.target.id == target)

            if entry and entry.user:
                if entry.user.bot:
                    return

                self.addSuspiciousAction(actionType, entry.user, guild.id)
                await self.checkSuspiciousAction(actionType, entry.user, guild.id)
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        await self.checkAudit(disnake.AuditLogAction.channel_delete, channel.id, "channels", channel.guild)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        await self.checkAudit(disnake.AuditLogAction.ban, user.id, "users", guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.checkAudit(disnake.AuditLogAction.kick, member.id, "users", member.guild)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        await self.checkAudit(disnake.AuditLogAction.role_delete, role.id, "roles", role.guild)

def setup(bot):
    bot.add_cog(AntiCrash(bot))
