print('✅ Admin criado: admin@enempro.com / Admin123!')

# Aluno
aluno = CustomUser.objects.create_user(
    username='aluno',
    email='aluno@enempro.com',
    password='Aluno123!',
    role='student',
    first_name='João',
    last_name='Silva'
)
print('✅ Aluno criado: aluno@enempro.com / Aluno123!')

# Corretor/Professor
corretor = CustomUser.objects.create_user(
    username='corretor',
    email='corretor@enempro.com',
    password='Corretor123!',
    role='teacher',
    first_name='Maria',
    last_name='Santos'
)
print('✅ Corretor criado: corretor@enempro.com / Corretor123!')

print('')
print('📋 RESUMO DOS USUÁRIOS:')
print('=' * 50)
print(f'👤 Admin    → admin@enempro.com    / Admin123!')
print(f'🎓 Aluno    → aluno@enempro.com    / Aluno123!')
print(f'✏️  Corretor → corretor@enempro.com / Corretor123!')
