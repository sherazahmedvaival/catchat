from catchat.models import User, Message
from catchat.extensions import db


def test_home_message_limit(client, app):
    amount = app.config['CATCHAT_MESSAGE_PER_PAGE']
    with app.app_context():
        user = User(email='test@example.com', nickname='tester')
        db.session.add(user)
        db.session.commit()
        for i in range(amount + 5):
            m = Message(author=user, body=f'message {i}')
            db.session.add(m)
        db.session.commit()

    response = client.get('/')
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert data.count('class="msg-box"') == amount
