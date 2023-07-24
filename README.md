# l-transcribe-api

This MVP was built to test some hypotheses for my friend's edtech startup. 

## Story 

- User uploads a recording of their lesson in English / Spanish language 
- It is transcribed using a supplied engine (currently, google transcribe api). 
- User later searches for specific words throughout all the recordings and has an opportunity to listen to them in the context (backend finds the word and cuts the audio \[t-5, t+5\] seconds from the word timestamp) -- analyse usecases, correct mistakes etc.

[![image.png](https://i.postimg.cc/YSV8XWgY/image.png)](https://postimg.cc/xkvK8q61)
[![image.png](https://i.postimg.cc/0jrk9hjL/image.png)](https://postimg.cc/QKGGb4pb)

## Technical

- Python + FastAPI + Alembic
- Self written (relly bad raw HTML frontend :) )
- docker-compose
- GitHub Secrets, GitHub Workflows

[![image.png](https://i.postimg.cc/SKqzmNh3/image.png)](https://postimg.cc/mPXrw4hy)
### TODO:
 - [ ] Change GitHub workflow from it simpliest form - clone repo, get secrets and run "docker compose up --build -d" on every push to main branch






