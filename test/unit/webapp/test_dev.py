from test.unit.webapp import client


def test_note(client):
    note = client.get('/dev/note')
    html = note.data.decode()
    assert 'Debugging Note for Developers' in html
    assert 'Your note here!' in html
