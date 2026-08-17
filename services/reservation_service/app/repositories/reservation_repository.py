from datetime import date

from app.core.config import get_config
from app.models.reservation import Reservation, ReservationStatus
from shared.repositories.db_repository import DBRepository
from shared.utils.exceptions import NoFetchedResultException


class ReservationRepository(DBRepository):
    def __init__(self):
        config = get_config()
        super().__init__("reservations", config)

    def save(self, reservation: Reservation) -> Reservation:
        query = f"""
            INSERT INTO {self._table_name} (
                listing_id,
                guest_id,
                check_in_date,
                check_out_date,
                total_price,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *;
        """

        return self._execute_fetch_one(
            query,
            Reservation,
            values=[
                reservation.listing_id,
                reservation.guest_id,
                reservation.check_in_date,
                reservation.check_out_date,
                reservation.total_price,
                reservation.status.value,
            ],
        )

    def find_by_id(
        self,
        reservation_id: int,
    ) -> Reservation | None:

        query = f"""
            SELECT *
            FROM {self._table_name}
            WHERE reservation_id = %s;
        """

        try:
            return self._execute_fetch_one(
                query,
                Reservation,
                values=[reservation_id],
            )
        except NoFetchedResultException:
            return None

    def find_all_by_guest_id(
        self,
        guest_id: int,
        status: ReservationStatus | None = None,
    ) -> list[Reservation]:

        values = [guest_id]

        query = f"""
            SELECT *
            FROM {self._table_name}
            WHERE guest_id = %s
        """

        if status is not None:
            query += " AND status = %s"
            values.append(status.value)

        query += " ORDER BY check_in_date;"

        return self._execute_fetch_all(
            query,
            Reservation,
            values=values,
        )

    def find_all_by_listing_id(
        self,
        listing_id: int,
        status: ReservationStatus | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[Reservation]:

        conditions = ["listing_id = %s"]
        values = [listing_id]

        if status is not None:
            conditions.append("status = %s")
            values.append(status.value)

        if start_date is not None:
            conditions.append("check_out_date > %s")
            values.append(start_date)

        if end_date is not None:
            conditions.append("check_in_date < %s")
            values.append(end_date)

        where_clause = " AND ".join(conditions)

        query = f"""
            SELECT *
            FROM {self._table_name}
            WHERE {where_clause}
            ORDER BY check_in_date;
        """

        return self._execute_fetch_all(
            query,
            Reservation,
            values=values,
        )

    def update(self, reservation: Reservation) -> Reservation:
        query = f"""
            UPDATE {self._table_name}
            SET
                check_in_date = %s,
                check_out_date = %s,
                total_price = %s,
                status = %s
            WHERE reservation_id = %s
            RETURNING *;
        """

        return self._execute_fetch_one(
            query,
            Reservation,
            values=[
                reservation.check_in_date,
                reservation.check_out_date,
                reservation.total_price,
                reservation.status.value,
                reservation.reservation_id,
            ],
        )

    def cancel(
        self,
        reservation_id: int,
    ) -> Reservation:

        query = f"""
            UPDATE {self._table_name}
            SET status = %s
            WHERE reservation_id = %s
            RETURNING *;
        """

        return self._execute_fetch_one(
            query,
            Reservation,
            values=[
                ReservationStatus.CANCELLED.value,
                reservation_id,
            ],
        )