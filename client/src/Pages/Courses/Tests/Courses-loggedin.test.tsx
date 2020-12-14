/* eslint-disable max-lines-per-function */
import { fireEvent } from '@testing-library/react';
import urls from 'Constants/urls';
import { rest } from 'msw';
import App from 'Pages/App/App';
import React from 'react';
import server from 'TestUtils/Mocks/server';
import { renderWithRouterAndProvider } from 'TestUtils/renderWith';

test('Renders two courses for non-error server response', async () => {
  // Note: mocked server response is handled by msw, in the src/mocks folder
  // and src/setupTests.js. The handler is set to return testCoursesJSONResponse
  // for /api/courses

  // render entire App so that we can check Loading and Error
  const screen = renderWithRouterAndProvider(<App />);

  // click the 'courses' tab to trigger the courses retrieval
  const coursesNavLink = screen.getByRole('tab', { name: /courses/ });
  fireEvent.click(coursesNavLink);
  // END: setup /////////////////////////////////////////

  // check loading spinner
  // note: the loading spinner has aria-hidden true whether or not it's visible >_<
  const loadingSpinner = await screen.findByRole('progressbar', { hidden: true });
  expect(loadingSpinner).toBeVisible();

  // check courses by looking for link on image
  // actual course details checked in Course.test.tsx
  const courses = await screen.findAllByRole('link', { name: /Course Image/ });
  expect(courses.length).toBe(2);

  // confirm loading spinner has disappeared
  const notLoadingSpinner = screen.queryByRole('progressbar', { hidden: true });
  expect(notLoadingSpinner).toBe(null);

  // confirm no error
  const errorAlert = screen.queryByRole('alert');
  expect(errorAlert).not.toBeInTheDocument();
});

test('Renders error alert for error server response', async () => {
  // override default msw response for review_quotes endpoint with error response
  server.resetHandlers(
    rest.get(urls.coursesURL,
      (req, res, ctx) => res(ctx.status(500), ctx.json({ message: 'oops' }))),
  );

  // render entire App so that we can check Loading and Error
  const screen = renderWithRouterAndProvider(<App />);

  // click the 'courses' tab to trigger the courses retrieval
  const coursesNavLink = screen.getByRole('tab', { name: /courses/ });
  fireEvent.click(coursesNavLink);
  // END: setup ///////////////////////////////////////

  // check loading spinner
  // note: the loading spinner has aria-hidden true whether or not it's visible >_<
  const loadingSpinner = await screen.findByRole('progressbar', { hidden: true });
  expect(loadingSpinner).toBeVisible();

  // confirm error
  const errorAlert = await screen.findByRole('alert');
  expect(errorAlert).toBeInTheDocument();

  // confirm loading spinner has disappeared
  const notLoadingSpinner = screen.queryByRole('progressbar', { hidden: true });
  expect(notLoadingSpinner).toBe(null);
});