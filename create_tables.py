from app.core.database import Base, engine
from app.models import user, task
Base.metadata.create_all(engine)