'use client';
import React, { useEffect, useState } from 'react';
import { fetchUser } from './api/fetchUser';

import { type UserAuth } from './types/UserAuth';
import { logger } from '@/utils/utils';

const fileLogger = logger.ns('userContext').seal();
const useUserLogger = fileLogger.ns('useUser').seal();

export function UserProvider({ children }: { children: React.ReactNode }) {
  // TODO
  return <div>{children}</div>;
}

export function useUser(): UserAuth {
  // TODO
  throw Error('Not implemented yet');
}
