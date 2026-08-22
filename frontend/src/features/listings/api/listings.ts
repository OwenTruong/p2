import { getAxios } from "@/utils/axios";
import type { Listing, ListingFormData, ListingQuery } from "../types";
import { baseListingPath, deleteListingPath, getListingDetailsPath, getMyListingsPath, updateListingPath } from "@/utils/config";
import axios from "axios";
import { ListingError } from "../errors/ListingError";


export async function getMyListings(): Promise<Listing[]> {

  try {

    const response = await getAxios().get<Listing[]>(
      getMyListingsPath
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

export async function getListings(query: ListingQuery = {}): Promise<Listing[]> {
  const params = new URLSearchParams();

  Object.entries(query).forEach(([key, value]) => {
    if (value !== undefined) {
      params.append(key, String(value));
    }
  });

  const response = await getAxios().get<Listing[]>(
    baseListingPath,
    {
      params: query,
    }
  );

  return response.data;
}

export async function getListingDetails(id: number): Promise<Listing> {
  const response = await getAxios().get<Listing>(
    getListingDetailsPath(id)
  );

  return response.data;
}

export async function createListing(
  data: ListingFormData
): Promise<void> {
  try {
    const response = await getAxios().post(
      baseListingPath,
      data
    );

    return response.data;

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

export async function updateListing(
  id: number,
  data: ListingFormData
): Promise<void> {
  try {
    const response = await getAxios().put(
      updateListingPath(id),
      data
    );

    return response.data;

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

export async function deleteListing(id: number): Promise<void> {
  try {
    await getAxios().delete(deleteListingPath(id));
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