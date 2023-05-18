import { useState, CSSProperties } from "react";
import ClipLoader from "react-spinners/ClipLoader";

const override = {
  display: "block",
  margin: "0 auto",
  borderColor: "red",
};

function App() {
  let [loading, setLoading] = useState(false);
  let [color, setColor] = useState("#FF9A5A");
  return (
    <div className="App">
      <ClipLoader
        color={color}
        loading={loading}
        cssOverride={override}
        size={50}
        aria-label="Loading Spinner"
        data-testid="loader"
      />
      <div className="submit" style={{display: "flex",justifyContent:"center",alignItems:"center"}}>
      <input type="file" id="video-file" name="video" accept="video/*"/>
       <input className="button-62" type="button" role="button" onClick={async (e)=>{
        const fileInput = document.querySelector('#video-file');
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('video', file);
        try{
          setLoading(true)
          const res = await fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData
        })
        setLoading(false)
        const text = await res.json()
        const videoText = document.querySelector('#text');
        
        videoText.value = text.text;
        console.log(text)
        }
        catch(e){
          setLoading(false)
          console.log(e.message);
        }
       }} value="Upload"/>
      </div>
      <div className="text">
       <textarea id="text" style={{width: "100%",height: "100%",borderRadius: "50px",outline:"none",border:"none",backgroundColor: "#282828",padding: "2rem",color: "white",fontSize:"1rem",fontWeight:"bold"}}/>
       </div>
    </div>
  );
}

export default App;
