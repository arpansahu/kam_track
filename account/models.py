from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

# Country code choices
COUNTRY_CODE_CHOICES = [
    ('+1', 'United States (+1)'),
    ('+7', 'Russia (+7)'),
    ('+20', 'Egypt (+20)'),
    ('+27', 'South Africa (+27)'),
    ('+30', 'Greece (+30)'),
    ('+31', 'Netherlands (+31)'),
    ('+32', 'Belgium (+32)'),
    ('+33', 'France (+33)'),
    ('+34', 'Spain (+34)'),
    ('+36', 'Hungary (+36)'),
    ('+39', 'Italy (+39)'),
    ('+40', 'Romania (+40)'),
    ('+41', 'Switzerland (+41)'),
    ('+43', 'Austria (+43)'),
    ('+44', 'United Kingdom (+44)'),
    ('+45', 'Denmark (+45)'),
    ('+46', 'Sweden (+46)'),
    ('+47', 'Norway (+47)'),
    ('+48', 'Poland (+48)'),
    ('+49', 'Germany (+49)'),
    ('+52', 'Mexico (+52)'),
    ('+54', 'Argentina (+54)'),
    ('+55', 'Brazil (+55)'),
    ('+56', 'Chile (+56)'),
    ('+57', 'Colombia (+57)'),
    ('+60', 'Malaysia (+60)'),
    ('+61', 'Australia (+61)'),
    ('+62', 'Indonesia (+62)'),
    ('+63', 'Philippines (+63)'),
    ('+64', 'New Zealand (+64)'),
    ('+65', 'Singapore (+65)'),
    ('+66', 'Thailand (+66)'),
    ('+81', 'Japan (+81)'),
    ('+82', 'South Korea (+82)'),
    ('+84', 'Vietnam (+84)'),
    ('+86', 'China (+86)'),
    ('+90', 'Turkey (+90)'),
    ('+91', 'India (+91)'),
    ('+92', 'Pakistan (+92)'),
    ('+93', 'Afghanistan (+93)'),
    ('+94', 'Sri Lanka (+94)'),
    ('+95', 'Myanmar (+95)'),
    ('+98', 'Iran (+98)'),
    ('+211', 'South Sudan (+211)'),
    ('+212', 'Morocco (+212)'),
    ('+213', 'Algeria (+213)'),
    ('+216', 'Tunisia (+216)'),
    ('+218', 'Libya (+218)'),
    ('+220', 'Gambia (+220)'),
    ('+221', 'Senegal (+221)'),
    ('+230', 'Mauritius (+230)'),
    ('+234', 'Nigeria (+234)'),
    ('+237', 'Cameroon (+237)'),
    ('+254', 'Kenya (+254)'),
    ('+255', 'Tanzania (+255)'),
    ('+256', 'Uganda (+256)'),
    ('+260', 'Zambia (+260)'),
    ('+263', 'Zimbabwe (+263)'),
    ('+358', 'Finland (+358)'),
    ('+374', 'Armenia (+374)'),
    ('+380', 'Ukraine (+380)'),
    ('+381', 'Serbia (+381)'),
    ('+382', 'Montenegro (+382)'),
    ('+385', 'Croatia (+385)'),
    ('+387', 'Bosnia and Herzegovina (+387)'),
    ('+420', 'Czech Republic (+420)'),
    ('+421', 'Slovakia (+421)'),
    ('+852', 'Hong Kong (+852)'),
    ('+853', 'Macau (+853)'),
    ('+855', 'Cambodia (+855)'),
    ('+856', 'Laos (+856)'),
    ('+880', 'Bangladesh (+880)'),
    ('+886', 'Taiwan (+886)'),
    ('+971', 'United Arab Emirates (+971)'),
    ('+972', 'Israel (+972)'),
    ('+973', 'Bahrain (+973)'),
    ('+974', 'Qatar (+974)'),
    ('+975', 'Bhutan (+975)'),
    ('+977', 'Nepal (+977)'),
    ('+992', 'Tajikistan (+992)'),
    ('+993', 'Turkmenistan (+993)'),
    ('+994', 'Azerbaijan (+994)'),
    ('+995', 'Georgia (+995)'),
    ('+996', 'Kyrgyzstan (+996)'),
    ('+998', 'Uzbekistan (+998)'),
]


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have a valid email")
        if not username:
            raise ValueError("User must have a valid username")
        if not password:
            raise ValueError("Enter a correct password")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.role = 'admin'
        user.is_active = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, default='profile_photos/default_profile_photo.png')

    # Role field
    ROLE_CHOICES = [
        ('kam', 'Key Account Manager'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='kam')


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return f"{self.name} ({self.email})"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_kam(self):
        return self.role == 'kam'

    @property
    def is_admin_user(self):
        return self.role == 'admin'