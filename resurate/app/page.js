import Body from '@/Components/Body';
import axios from 'axios'

const page = async () => {
  const res = await axios.get('http://127.0.0.1:3000/');
  const data = res.data

  // console.log(data.Email)
  return (
    <div>
      <Body/>
      <h1 className='text-red-500 text-2xl'>{data.Catagory}</h1>
    </div>
  )
}

export default page
