import os
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

test_client = TestClient(app)

TEST_DIR = str(Path(__file__).resolve().parent)


def test_get_memes():
    response = test_client.get('/memes')
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert isinstance(data['message'], list)


def test_save_meme():
    files = {'file': ('test1.jpg', open(os.path.join(TEST_DIR, 'test_files', 'test1.jpg'), 'rb'),
                      'image/jpeg')}
    response = test_client.post('/memes', data={'description': 'test1'},
                                files=files)
    assert response.status_code == 200
    assert response.json() == {'message': 'Success'}


def test_duplicate_meme():
    files = {'file': ('test1.jpg', open(os.path.join(TEST_DIR, 'test_files', 'test1.jpg'), 'rb'),
                      'image/jpeg')}
    response = test_client.post('/memes', data={'description': 'test1'},
                                files=files)
    assert response.status_code == 400
    assert response.json() == {
        'detail': {
            'filename': [
                'A meme with the same name already exists'
            ]
        }
    }
