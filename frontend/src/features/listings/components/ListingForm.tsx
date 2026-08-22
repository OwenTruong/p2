import { useState } from "react";
import { useNavigate } from "react-router-dom";

import type { ListingFormData } from "../types";
import { ListingError } from "../errors/ListingError";

import styles from "./ListingForm.module.css";

interface ListingFormProps {
  initialValues?: Partial<ListingFormData>;
  onSubmit: (data: ListingFormData) => Promise<void>;
  submitLabel?: string;
}

type FieldErrors = {
  title?: string;
  description?: string;
  price_per_night?: string;
  url?: string;
  max_guests?: string;
  bedrooms?: string;
  bathrooms?: string;
  address?: string;
  city?: string;
  state?: string;
  zip_code?: string;
};

const defaultValues: ListingFormData = {
  title: "",
  description: "",
  price_per_night: 0,
  url: "",
  max_guests: 1,
  bedrooms: 1,
  bathrooms: 1,
  address: "",
  city: "",
  state: "",
  zip_code: "",
  is_published: false,
};

export default function ListingForm({
  initialValues,
  onSubmit,
  submitLabel = "Save Listing",
}: ListingFormProps) {
  const navigate = useNavigate();

  const [form, setForm] = useState<ListingFormData>({
    ...defaultValues,
    ...initialValues,
  });

  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [formError, setFormError] = useState<string[] | null>(null);
  const [submitting, setSubmitting] = useState(false);

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) {
    const { name, value, type } = e.target;

    setForm((prev) => ({
      ...prev,
      [name]:
        type === "checkbox"
          ? (e.target as HTMLInputElement).checked
          : type === "number"
            ? Number(value)
            : value,
    }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (submitting) return;

    const errors = validateListing(form);

    if (Object.keys(errors).length > 0) {
      setFieldErrors(errors);
      return;
    }

    setFieldErrors({});
    setFormError(null);
    setSubmitting(true);

    try {
      await onSubmit(form);

      navigate("/my-listings", { replace: true });
    } catch (error) {
      setFormError(
        error instanceof ListingError
          ? error.errors.map((err) => err.message)
          : ["An unexpected error occurred. Please try again later."]
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form
      className={styles.form}
      onSubmit={handleSubmit}
      noValidate
    >
      <h2 className={styles.title}>{submitLabel}</h2>

      {formError && (
        <div className={styles.alert} role="alert">
          <ul>
            {formError.map((error, i) => (
              <li key={i}>{error}</li>
            ))}
          </ul>
        </div>
      )}

      <section className={styles.section}>
        <h3>Basic Information</h3>

        <div className={styles.field}>
          <label htmlFor="title">Title</label>

          <input
            id="title"
            name="title"
            value={form.title}
            onChange={handleChange}
            aria-invalid={!!fieldErrors.title || undefined}
            aria-describedby={
              fieldErrors.title ? "title-error" : undefined
            }
          />

          {fieldErrors.title && (
            <p
              id="title-error"
              className={styles.fieldError}
            >
              {fieldErrors.title}
            </p>
          )}
        </div>

        <div className={styles.field}>
          <label htmlFor="description">Description</label>

          <textarea
            id="description"
            name="description"
            value={form.description}
            onChange={handleChange}
            rows={5}
            aria-invalid={
              !!fieldErrors.description || undefined
            }
            aria-describedby={
              fieldErrors.description
                ? "description-error"
                : undefined
            }
          />

          {fieldErrors.description && (
            <p
              id="description-error"
              className={styles.fieldError}
            >
              {fieldErrors.description}
            </p>
          )}
        </div>
      </section>

      <section className={styles.section}>
        <h3>Property Details</h3>

        <div className={styles.grid}>
          <div className={styles.field}>
            <label htmlFor="price_per_night">
              Price per night
            </label>

            <input
              id="price_per_night"
              name="price_per_night"
              type="number"
              step="0.01"
              value={form.price_per_night}
              onChange={handleChange}
              aria-invalid={
                !!fieldErrors.price_per_night || undefined
              }
              aria-describedby={
                fieldErrors.price_per_night
                  ? "price-error"
                  : undefined
              }
            />

            {fieldErrors.price_per_night && (
              <p
                id="price-error"
                className={styles.fieldError}
              >
                {fieldErrors.price_per_night}
              </p>
            )}
          </div>

          <div className={styles.field}>
            <label htmlFor="max_guests">
              Max guests
            </label>

            <input
              id="max_guests"
              name="max_guests"
              type="number"
              value={form.max_guests}
              onChange={handleChange}
              aria-invalid={
                !!fieldErrors.max_guests || undefined
              }
              aria-describedby={
                fieldErrors.max_guests
                  ? "max-guests-error"
                  : undefined
              }
            />

            {fieldErrors.max_guests && (
              <p
                id="max-guests-error"
                className={styles.fieldError}
              >
                {fieldErrors.max_guests}
              </p>
            )}
          </div>

          <div className={styles.field}>
            <label htmlFor="bedrooms">
              Bedrooms
            </label>

            <input
              id="bedrooms"
              name="bedrooms"
              type="number"
              value={form.bedrooms}
              onChange={handleChange}
              aria-invalid={
                !!fieldErrors.bedrooms || undefined
              }
              aria-describedby={
                fieldErrors.bedrooms
                  ? "bedrooms-error"
                  : undefined
              }
            />

            {fieldErrors.bedrooms && (
              <p
                id="bedrooms-error"
                className={styles.fieldError}
              >
                {fieldErrors.bedrooms}
              </p>
            )}
          </div>

          <div className={styles.field}>
            <label htmlFor="bathrooms">
              Bathrooms
            </label>

            <input
              id="bathrooms"
              name="bathrooms"
              type="number"
              step="0.5"
              value={form.bathrooms}
              onChange={handleChange}
              aria-invalid={
                !!fieldErrors.bathrooms || undefined
              }
              aria-describedby={
                fieldErrors.bathrooms
                  ? "bathrooms-error"
                  : undefined
              }
            />

            {fieldErrors.bathrooms && (
              <p
                id="bathrooms-error"
                className={styles.fieldError}
              >
                {fieldErrors.bathrooms}
              </p>
            )}
          </div>
        </div>
      </section>

      <section className={styles.section}>
        <h3>Address</h3>

        <div className={styles.field}>
          <label htmlFor="address">Address</label>

          <input
            id="address"
            name="address"
            value={form.address}
            onChange={handleChange}
            aria-invalid={
              !!fieldErrors.address || undefined
            }
            aria-describedby={
              fieldErrors.address
                ? "address-error"
                : undefined
            }
          />

          {fieldErrors.address && (
            <p
              id="address-error"
              className={styles.fieldError}
            >
              {fieldErrors.address}
            </p>
          )}
        </div>

        <div className={styles.addressGrid}>
          <div className={styles.field}>
            <label htmlFor="city">City</label>

            <input
              id="city"
              name="city"
              value={form.city}
              onChange={handleChange}
              aria-invalid={
                !!fieldErrors.city || undefined
              }
              aria-describedby={
                fieldErrors.city
                  ? "city-error"
                  : undefined
              }
            />

            {fieldErrors.city && (
              <p
                id="city-error"
                className={styles.fieldError}
              >
                {fieldErrors.city}
              </p>
            )}
          </div>

          <div className={styles.field}>
            <label htmlFor="state">State</label>

            <input
              id="state"
              name="state"
              value={form.state}
              onChange={handleChange}
              maxLength={2}
              aria-invalid={
                !!fieldErrors.state || undefined
              }
              aria-describedby={
                fieldErrors.state
                  ? "state-error"
                  : undefined
              }
            />

            {fieldErrors.state && (
              <p
                id="state-error"
                className={styles.fieldError}
              >
                {fieldErrors.state}
              </p>
            )}
          </div>

          <div className={styles.field}>
            <label htmlFor="zip_code">
              ZIP code
            </label>

            <input
              id="zip_code"
              name="zip_code"
              value={form.zip_code}
              onChange={handleChange}
              aria-invalid={
                !!fieldErrors.zip_code || undefined
              }
              aria-describedby={
                fieldErrors.zip_code
                  ? "zip-code-error"
                  : undefined
              }
            />

            {fieldErrors.zip_code && (
              <p
                id="zip-code-error"
                className={styles.fieldError}
              >
                {fieldErrors.zip_code}
              </p>
            )}
          </div>
        </div>
      </section>

      <section className={styles.section}>
        <h3>Photo</h3>

        <div className={styles.field}>
          <label htmlFor="url">
            Photo URL
          </label>

          <input
            id="url"
            name="url"
            type="url"
            placeholder="https://example.com/photo.jpg"
            value={form.url}
            onChange={handleChange}
            aria-invalid={
              !!fieldErrors.url || undefined
            }
            aria-describedby={
              fieldErrors.url
                ? "photo-url-error"
                : undefined
            }
          />

          {fieldErrors.url && (
            <p
              id="photo-url-error"
              className={styles.fieldError}
            >
              {fieldErrors.url}
            </p>
          )}
        </div>

        {form.url && (
          <div className={styles.photoPreview}>
            <img
              src={form.url}
              alt="Listing preview"
            />
          </div>
        )}
      </section>
      <label className={styles.checkbox}>
        <input
          name="is_published"
          type="checkbox"
          checked={form.is_published}
          onChange={handleChange}
        />

        Publish this listing
      </label>

      <div className={styles.actions}>
        <button
          type="submit"
          disabled={submitting}
        >
          {submitting ? "Saving..." : submitLabel}
        </button>
      </div>
    </form>
  );
}

function validateListing(
  form: ListingFormData
): FieldErrors {
  const errors: FieldErrors = {};

  const title = form.title.trim();
  const description = form.description.trim();
  const address = form.address.trim();
  const city = form.city.trim();
  const state = form.state.trim();
  const zipCode = form.zip_code.trim();

  if (!title) {
    errors.title = "Title is required.";
  } else if (title.length < 3) {
    errors.title = "Title must be at least 3 characters.";
  } else if (title.length > 100) {
    errors.title = "Title must be at most 100 characters.";
  }

  if (description.length > 1000) {
    errors.description =
      "Description must be at most 1000 characters.";
  }

  if (form.price_per_night <= 0) {
    errors.price_per_night =
      "Price per night must be greater than 0.";
  }

  if (form.max_guests < 1) {
    errors.max_guests =
      "Maximum guests must be at least 1.";
  }

  if (form.bedrooms < 1) {
    errors.bedrooms =
      "Bedrooms must be at least 1.";
  }

  if (form.bathrooms < 1) {
    errors.bathrooms =
      "Bathrooms must be at least 1.";
  }

  if (!address) {
    errors.address = "Address is required.";
  }

  if (!city) {
    errors.city = "City is required.";
  }

  if (!state) {
    errors.state = "State is required.";
  } else if (!/^[A-Za-z]{2}$/.test(state)) {
    errors.state =
      "State must be a 2-letter abbreviation.";
  }

  if (!zipCode) {
    errors.zip_code = "ZIP code is required.";
  } else if (!/^\d{5}(-\d{4})?$/.test(zipCode)) {
    errors.zip_code =
      "Enter a valid ZIP code.";
  }

  return errors;
}