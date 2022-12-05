import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { useEffect, useState } from 'react';

export default function Home() {
  const [data, setData] = useState([{}]);
  const [loading, setLoading] = useState(true);

  function fetchData() {
    setLoading(true);
    fetch('/api/list')
      .then((response) => response.status === 200 ? response.json() : [])
      .then((data) => {
        setData(data);
        setLoading(false)
      });
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }
  else if (!data || data.length === 0) {
    return <div class="errorMessage"><h2>Failed to load</h2></div>;
  }
  return (
    <div className={styles.container}>
      <Head>
        <title>Listy</title>
        <meta name="description" content="I list things!" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1>Scoreboard</h1>

        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
            <TableHead>
              <TableRow >
                <TableCell align="left">Rank</TableCell>
                <TableCell>Username</TableCell>
                <TableCell align="right">Points</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((row) => (
                <TableRow
                  key={row.name}
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell align="right">{row.rank}</TableCell>
                  <TableCell scope="row">
                    {row.username}
                  </TableCell>
                  <TableCell align="right">{row.points}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </main>
    </div>
  )
}
