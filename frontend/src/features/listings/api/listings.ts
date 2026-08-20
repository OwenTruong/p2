import { getAxios } from "@/utils/axios";
import type { Listing } from "../types";
import { getListingsPath } from "@/utils/config";
import axios from "axios";
import { ListingError } from "../errors/ListingError";


export async function getMyListings(): Promise<Listing[]> {

  try {

    const response = await getAxios().get<Listing[]>(
      getListingsPath
    );

    return response.data

  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new ListingError(
        error.response.status,
        error.response.data
      );
    }

    throw error;
  }
}
