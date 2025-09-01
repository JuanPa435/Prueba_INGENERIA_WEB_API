from repositories.band_repository import BandRepository
from models.band_model import Band
from sqlalchemy.orm import Session

class BandService:

    def __init__(self, db_session: Session):
        self.repository = BandRepository(db_session)

    def listar_bandas(self):
        return self.repository.get_all_bands()

    def obtener_banda(self, band_id: int):
        return self.repository.get_band_by_id(band_id)

    def crear_banda(self, name: str):
        return self.repository.create_band(name)

    def actualizar_banda(self, band_id: int, name: str = None):
        return self.repository.update_band(band_id, name)

    def eliminar_banda(self, band_id: int):
        return self.repository.delete_band(band_id)