'use client';
import { isSessionValid } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    if (!isSessionValid()) {
      router.push('/login');
    }
  }, []);

  const url =
    'https://app.powerbi.com/reportEmbed?reportId=8ae8e760-1471-495f-a032-dc2e9bfd8ec7&autoAuth=true&ctid=2dff09ac-2b3b-4182-9953-2b548e0d0b39&filterPaneEnabled=false&navContentPaneEnabled=false';

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '90vh',
        width: '90vw',
        overflow: 'hidden', // Ẩn mọi phần nội dung thừa
        padding: 0,
        marginLeft:'60px'
      }}
    >
      <iframe
        title="Power BI Dashboard"
        style={{
          border: 'none',
          width: '95%', // Đảm bảo vừa khung ngang
          height: '95%', // Đảm bảo vừa khung dọc
          overflow: 'hidden',
        }}
        src={url}
      />
    </div>
  );
}
