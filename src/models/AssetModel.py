from .BaseDataModel import BaseDataModel
from .db_schemas import Asset
from .enums.DataBaseEnum import DataBaseEnum
from bson import ObjectId
from sqlalchemy.future import select


class AssetModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        # self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        # await instance.init_collection()
        return instance

    # async def init_collection(self):
    #     all_collection = await self.db_client.list_collection_names()

    #     if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collection:
    #         self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
    #         indexes = Asset.get_indexes()
    #         for index in indexes:
    #             await self.collection.create_index(
    #                 index["key"],
    #                 name=index["name"],
    #                 unique=index["unique"]
    #             )

    async def create_asset(self, asset: Asset):
        async with self.db_client() as session:
            async with session.begin():
                session.add(asset)
            await session.commit()
            await session.refresh(asset)
        return asset

        # result = await self.collection.insert_one(asset.model_dump(by_alias=True, exclude_unset= True))
        # asset.id = result.inserted_id

        # return asset

    async def get_all_project_assets(self, asset_project_id: str, asset_type: str):
        async with self.db_client() as session:
            async with session.begin():
                stmt = select(Asset).where(
                    Asset.asset_project_id == asset_project_id,
                    Asset.asset_type == asset_type,
                )

                results = await session.execute(stmt)
                records = results.scalars().all()
        return records

        # records = await self.collection.find({
        #     "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id,
        #     "asset_type":asset_type
        # }).to_list(length= None)

        # return [
        #     Asset(**rec)
        #     for rec in records
        # ]

    async def get_asset_record(self, asset_project_id: str, asset_name: str):
        async with self.db_client() as session:
            async with session.begin():
                stmt = select(Asset).where(
                    Asset.asset_project_id == asset_project_id,
                    Asset.asset_name == asset_name,
                )
                result = await session.execute(stmt)
                records = result.scalar_one_or_none()
        return records

        # record = await self.collection.find_one({
        #     "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id,
        #     "asset_name":asset_name,
        # })

        # if record:
        #     return Asset(**record)

        # return None
