from django.db import models

class Role(models.Model):
    libelle = models.CharField(max_length=254, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.libelle

class Notification(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='demandes')
    content = models.TextField(null=True)  # Assuming content should be textual
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification {self.id}"

class User(models.Model):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users')
    code_user = models.CharField(max_length=254, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code_user