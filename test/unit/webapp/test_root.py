from test.unit.webapp import client


def test_landing(client):
    landing = client.get("/")
    html = landing.data.decode()

    # Check that links to `about` and `login` pages exist
    assert "<a href=\"/about/\">About</a>" in html
    assert " <a href=\"/home/\">Login</a>" in html

    # Spot check important text
    assert "At CultureMesh, we're building networks to match these " \
           "real-world dynamics and knit the diverse fabrics of our world " \
           "together." in html
    assert "1. Join a network you belong to." in html

    assert landing.status_code == 200


def test_landing_aliases(client):
    landing = client.get("/")
    assert client.get("/index/").data == landing.data


def test_about(client):
    about = client.get('/about/')
    html = about.data.decode()

    print(html)
    assert 'About CultureMesh' in html
    assert 'CultureMesh is building networks to match the' in html
    assert 'Ken Chester' in html
    assert 'img src="https://www.culturemesh.com/internal/team/Ken_Chester.jpg"' in html

    assert about.status_code == 200
