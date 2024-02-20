import { SignInButton, SignedOut, UserButton } from "@clerk/nextjs";
import Link from "next/link";


const Header = () => {
  return (
    <header className="bg-white fixed top-0 left-0 w-screen lg:w-[calc(100vw-0.7rem)] shadow-md lg:px-40 z-40">
      <div className="mx-auto flex h-16 w-full items-center justify-between gap-8 px-4 sm:px-6 lg:px-8">
        <Link className=" text-teal-600 flex items-center justify-center" href="/">
          <p className="text-xl font-bold uppercase text-[#402aff] hidden lg:block">Resurate</p>
        </Link>

        <div className="flex items-center justify-end md:justify-between">
          <div className="flex items-center gap-4">
            <div className="sm:flex sm:gap-4 flex items-center justify-end gap-4">
              <UserButton afterSignOutUrl="/" />

              <SignedOut>
                <SignInButton afterSignInUrl="/" mode="modal" className='bg-primary rounded px-4 py-2 text-white' />
              </SignedOut>
            </div>
          </div>
        </div>
      </div>
    </header>



  )
}

export default Header
