import Box from '@material-ui/core/Box';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import AddButton from 'Pages/Common/AddButton';
import React, { ReactElement, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { setReviewQuotes, setReviewQuotesFromServer } from './Redux/actions';
import ReviewQuote from './ReviewQuote';
import { ReviewQuoteType } from './Types';

// eslint-disable-next-line max-lines-per-function
export default function ReviewQuotes(): ReactElement {
  const dispatch = useDispatch();
  const reviewQuotes = useSelector((state) => state.reviewQuotes);
  console.log('reviewQuotes!', reviewQuotes);

  // const user = useSelector((state) => state.user);
  const user = true; // TODO: <------------ for testing only!!!

  // populate review quotes data from the server
  useEffect(() => { dispatch(setReviewQuotesFromServer()); }, [dispatch]);

  const addQuote = () => {
    const newQuote: ReviewQuoteType = { body: '', id: 0 - reviewQuotes.length - 1 };
    dispatch(setReviewQuotes([...reviewQuotes, newQuote]));
  };

  return (
    <Box component="section" mt={4} mb={4} p={2} pt={2}>
      <Typography variant="h2" gutterBottom>
        Students say...
      </Typography>
      <Grid container spacing={3}>
        {reviewQuotes.map((quote) => (
          <ReviewQuote
            key={quote.id}
            quoteData={quote}
            editable={user !== null}
          />
        ))}
        {user ? <AddButton onClick={addQuote} /> : null}
      </Grid>
    </Box>
  );
}