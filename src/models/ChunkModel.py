from .BaseDataModel import BaseDataModel
from .db_schemas import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne
from sqlalchemy.future import select
from sqlalchemy import func, delete


class ChunkModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        # self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        # await instance.init_collection()
        return instance

    # async def init_collection(self):
    #     all_collection = await self.db_client.list_collection_names()
    #     if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collection:
    #         self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
    #         indexes = DataChunk.get_indexes()
    #         for index in indexes:
    #             await self.collection.create_index(
    #                 index["key"],
    #                 name=index["name"],
    #                 unique=index["unique"]
    #             )

    async def insert_chunk(self, chunk: DataChunk):
        async with self.db_client() as session:
            async with session.begin():
                session.add(chunk)
            await session.commit()
            await session.refresh(chunk)

        return chunk

        # result = await self.collection.insert_one(chunk.model_dump(by_alias=True, exclude_unset= True))
        # chunk._id = result.inserted_id
        # return chunk

    async def get_chunk(self, chunk_id: str):
        async with self.db_client() as session:
            async with session.begin():
                result = await session.execute(
                    select(DataChunk).where(DataChunk.chunk_id == chunk_id)
                )
                chunk = result.scalar_one_or_none()
            return chunk

        # result = await self.collection.find_one({
        #     "_id": ObjectId(chunk_id)
        # })

        # if result is None:
        #     return None

        # return DataChunk(**result)

    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):
        async with self.db_client() as session:
            async with session.begin():
                for i in range(0, len(chunks), batch_size):
                    batch = chunks[i : i + batch_size]
                    session.add_all(batch)
            await session.commit()
        return len(chunks)

        # for i in range(0, len(chunks), batch_size):
        #     batch = chunks[i:i+batch_size]

        #     operations = [
        #         InsertOne(chunk.model_dump(by_alias=True, exclude_unset= True))
        #         for chunk in batch
        #     ]

        #     await self.collection.bulk_write(operations)

        # return len(chunks)

    async def delete_chunks_by_project_id(self, project_id: ObjectId):
        async with self.db_client() as session:
            async with session.begin():
                stmt = delete(DataChunk).where(DataChunk.chunk_project_id == project_id)
                result = await session.execute(stmt)
                await session.commit()
        return result.rowcount

        # result = await self.collection.delete_many({"chunk_project_id": project_id})

        # return result.deleted_count  # Return the number of deleted documents

    async def get_project_chunks(
        self, project_id: ObjectId, page_no: int = 1, page_size: int = 50
    ):
        async with self.db_client() as session:
            async with session.begin():
                stmt = (
                    select(DataChunk)
                    .where(DataChunk.chunk_project_id == project_id)
                    .offset((page_no - 1) * page_size)
                    .limit(page_size)
                )
                result = await session.execute(stmt)
                records = result.scalars().all()
        return records

        # records = (
        #     await self.collection.find({"chunk_project_id": project_id})
        #     .skip((page_no - 1) * page_size)
        #     .limit(page_size)
        #     .to_list(length=None)
        # )

        # return [DataChunk(**record) for record in records]
