from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Category, Tag, Post, Comment, PostLike


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Author Status & Profile', {'fields': ('is_author', 'bio')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Author Status & Profile', {'fields': ('is_author', 'bio')}),
    )
    list_display = ('username', 'email', 'is_author', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('is_author', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    actions = ['promote_to_author', 'revoke_author_status']

    @admin.action(description="Promote selected users to Author status")
    def promote_to_author(self, request, queryset):
        updated = queryset.update(is_author=True)
        self.message_user(request, f"{updated} user(s) successfully promoted to Author.")

    @admin.action(description="Revoke Author status from selected users")
    def revoke_author_status(self, request, queryset):
        updated = queryset.update(is_author=False)
        self.message_user(request, f"Author status revoked for {updated} user(s).")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'view_count', 'created_at', 'updated_at')
    list_filter = ('status', 'category', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    date_hierarchy = 'created_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'short_text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__title', 'text')

    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Comment Text'


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__title')
